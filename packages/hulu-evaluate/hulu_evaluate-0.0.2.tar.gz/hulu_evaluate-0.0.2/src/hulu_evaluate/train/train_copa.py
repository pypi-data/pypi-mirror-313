import torch
from sklearn.metrics import matthews_corrcoef
from torch import amp, nn
from torch.nn import CrossEntropyLoss
from tqdm import tqdm
from transformers import AdamW, AutoModel, get_linear_schedule_with_warmup

from hulu_evaluate.hulu_arguments.train_arguments import HuluArgument
from hulu_evaluate.train.common_helper import write_submission
from hulu_evaluate.train.lora_helper import set_lora


def compute_mcc(preds, labels):
    preds = preds.cpu().numpy()
    labels = labels.cpu().numpy()
    return matthews_corrcoef(labels, preds)


class AutoForMultipleChoice(nn.Module):
    def __init__(self, model_name):
        super().__init__()
        self.model = AutoModel.from_pretrained(model_name)

        self.classifier = nn.Linear(self.model.config.hidden_size, 1)

    def forward(self, input_ids, attention_mask=None, labels=None):
        batch_size, num_choices, seq_length = input_ids.shape
        input_ids = input_ids.view(-1, seq_length)

        attention_mask = (
            attention_mask.view(-1, seq_length) if attention_mask is not None else None
        )
        outputs = self.model(
            input_ids,
            attention_mask=attention_mask,
            return_dict=True,
            output_hidden_states=True,
        )
        pooled_output = outputs.hidden_states[-1][:, -1, :]

        logits = self.classifier(pooled_output).view(batch_size, num_choices)

        if labels is not None:
            loss_fct = CrossEntropyLoss()
            loss = loss_fct(logits, labels)
            return loss, logits
        return logits  # prediction mode


class CopaTrainPipeline:
    def __init__(self, hulu_args: HuluArgument):
        self.device = (
            torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        )
        self.hulu_args = hulu_args
        self.train_loader, self.dev_loader, self.test_loader = None, None, None

    def set_tokenized_datasets(self, train_loader, dev_loader, test_loader):
        self.train_loader, self.dev_loader, self.test_loader = (
            train_loader,
            dev_loader,
            test_loader,
        )

    def load_model(self):
        model = AutoForMultipleChoice(self.hulu_args.model_name)

        if self.hulu_args.use_lora:
            model = set_lora(self.hulu_args, sequente_classification=False, model=model)

        model.to(self.device)
        return model

    def training(self):

        model = self.load_model()

        use_fp16 = self.hulu_args.precision == "fp16"
        scaler = amp.GradScaler() if use_fp16 else None
        device_type = "cuda" if torch.cuda.is_available() else "cpu"

        optimizer = AdamW(model.parameters(), lr=self.hulu_args.train_lr)
        total_steps = len(self.train_loader) * self.hulu_args.train_batch
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=self.hulu_args.train_warmup,
            num_training_steps=total_steps,
        )

        num_eval_steps = len(self.train_loader) // 3
        step = 0

        for epoch in range(self.hulu_args.train_epochs):
            model.train()
            total_loss, correct_preds = 0, 0

            for batch in tqdm(
                self.train_loader,
                desc=f"Training Epoch {epoch + 1}/{self.hulu_args.train_epochs}",
            ):
                step += 1
                input_ids, attention_mask, labels = (
                    batch["input_ids"].to(self.device),
                    batch["attention_mask"].to(self.device),
                    batch["label"].to(self.device),
                )

                optimizer.zero_grad()

                with amp.autocast(device_type=device_type, enabled=use_fp16):
                    loss, logits = model(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        labels=labels,
                    )

                if use_fp16:
                    scaler.scale(loss).backward()
                    scaler.step(optimizer)
                    scaler.update()
                else:
                    loss.backward()
                    optimizer.step()

                scheduler.step()
                total_loss += loss.item()
                correct_preds += (logits.argmax(dim=1) == labels).sum().item()

                if step % num_eval_steps == 0:
                    eval_loss, eval_acc, eval_mcc = self.evaluate(model)
                    print(
                        f"Step {step}: Eval Loss = {eval_loss:.4f}, Eval Acc = {eval_acc:.4f}, Eval MCC = {eval_mcc:.4f}"
                    )

            avg_loss = total_loss / len(self.train_loader)
            accuracy = correct_preds / len(self.train_loader.dataset)
            print(
                f"Epoch {epoch + 1}: Train Loss = {avg_loss:.4f}, Train Accuracy = {accuracy:.4f}"
            )

        return model

    def evaluate(self, model):
        model.eval()
        total_loss, correct_preds = 0, 0
        all_preds, all_labels = [], []

        with torch.no_grad():
            for _, batch in enumerate(self.dev_loader):
                input_ids, attention_mask, labels = (
                    batch["input_ids"].squeeze(1).to(self.device),
                    batch["attention_mask"].squeeze(1).to(self.device),
                    batch["label"].to(self.device),
                )

                loss, logits = model(
                    input_ids=input_ids, attention_mask=attention_mask, labels=labels
                )
                total_loss += loss.item()
                preds = logits.argmax(dim=1)
                correct_preds += (preds == labels).sum().item()

                all_preds.append(preds)
                all_labels.append(labels)

        avg_loss = total_loss / len(self.dev_loader)
        accuracy = correct_preds / len(self.dev_loader.dataset)

        all_preds = torch.cat(all_preds)
        all_labels = torch.cat(all_labels)
        mcc = compute_mcc(all_preds, all_labels)
        return avg_loss, accuracy, mcc

    def create_submission(self, model):
        model.eval()
        predictions_data = []

        with torch.no_grad():
            for idx, batch in enumerate(self.test_loader):
                input_ids, attention_mask = batch["input_ids"].to(self.device), batch[
                    "attention_mask"
                ].to(self.device)

                logits = model(input_ids=input_ids, attention_mask=attention_mask)
                preds = logits.argmax(dim=1)

                for i, prediction in enumerate(preds):
                    predictions_data.append(
                        {
                            "id": idx * self.test_loader.batch_size + i,
                            "label": str((prediction.item() + 1)),
                        }
                    )

        write_submission(
            task="copa",
            predictions_data=predictions_data,
            output_dir=self.hulu_args.output_dir,
        )
