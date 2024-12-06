import evaluate
import numpy as np
import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)

from hulu_evaluate.hulu_arguments import HuluArgument
from hulu_evaluate.train.common_helper import write_submission
from hulu_evaluate.train.constants import CB_LABELS, SST_LABELS
from hulu_evaluate.train.lora_helper import set_lora


class HuluTrainPipeline:

    def __init__(
        self,
        hulu_args: HuluArgument,
        current_task: str,
    ):
        self.hulu_args = hulu_args
        self.current_task = current_task

        self.tokenized_train_dataset = None
        self.tokenized_dev_dataset = None
        self.tokenized_test_dataset = None

    def set_tokenized_datasets(
        self, tokenized_train_dataset, tokenized_dev_dataset, tokenized_test_dataset
    ):
        self.tokenized_train_dataset = tokenized_train_dataset
        self.tokenized_dev_dataset = tokenized_dev_dataset
        self.tokenized_test_dataset = tokenized_test_dataset

    def get_eval_count(self):
        train_dataset_size = len(self.tokenized_train_dataset)
        batch_size_per_device = self.hulu_args.train_batch
        steps_per_epoch = train_dataset_size // batch_size_per_device

        # evaluation 3 times in each epoch
        eval_steps = steps_per_epoch // 3
        return eval_steps

    def set_model_and_tokenizer(self):
        model_kwargs = (
            {"num_labels": 3}
            if self.current_task in ["sst", "cb"]
            else {"num_labels": 2}
        )
        model = AutoModelForSequenceClassification.from_pretrained(
            self.hulu_args.model_name, **model_kwargs
        )

        tokenizer = AutoTokenizer.from_pretrained(self.hulu_args.tokenizer_name)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            model.config.pad_token_id = model.config.eos_token_id

        return model, tokenizer

    def training(self):

        device = (
            torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        )

        model, tokenizer = self.set_model_and_tokenizer()

        if self.hulu_args.use_lora:
            model = set_lora(self.hulu_args, sequente_classification=True, model=model)

        model.to(device)
        data_collator = DataCollatorWithPadding(tokenizer=tokenizer, padding=True)

        accuracy_metric = evaluate.load("accuracy")
        mcc_metric = evaluate.load("matthews_correlation")
        f1_metric = evaluate.load("f1")

        def compute_metrics(eval_pred):
            logits, labels = eval_pred

            predictions = np.argmax(logits, axis=-1)

            accuracy = accuracy_metric.compute(
                predictions=predictions, references=labels
            )
            f1 = f1_metric.compute(
                predictions=predictions, references=labels, average="weighted"
            )
            mcc = mcc_metric.compute(predictions=predictions, references=labels)

            return {
                "accuracy": accuracy["accuracy"],
                "mcc": mcc["matthews_correlation"],
                "f1": f1["f1"],
            }

        training_args = TrainingArguments(
            output_dir=self.hulu_args.output_dir,
            learning_rate=self.hulu_args.train_lr,
            per_device_train_batch_size=self.hulu_args.train_batch,
            per_device_eval_batch_size=self.hulu_args.train_batch,
            num_train_epochs=self.hulu_args.train_epochs,
            eval_strategy="steps",
            eval_steps=self.get_eval_count(),
            logging_steps=self.get_eval_count(),
            warmup_steps=self.hulu_args.train_warmup,
            fp16=self.hulu_args.precision == "fp16",
            save_strategy="no",
            load_best_model_at_end=False,
            save_safetensors=False,
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=self.tokenized_train_dataset,
            eval_dataset=self.tokenized_dev_dataset,
            tokenizer=tokenizer,
            data_collator=data_collator,
            compute_metrics=compute_metrics,
        )

        trainer.train()
        return trainer

    def create_submission(self, trainer):
        hulu_results = trainer.predict(self.tokenized_test_dataset)
        predictions = np.argmax(hulu_results.predictions, axis=-1)

        if self.current_task == "sst":
            reverse_labels = {v: k for k, v in SST_LABELS.items()}
        elif self.current_task == "cb":
            reverse_labels = {v: k for k, v in CB_LABELS.items()}
        else:
            reverse_labels = None

        predictions_data = [
            {
                "id": str(i),
                "label": reverse_labels[pred] if reverse_labels else str(pred),
            }
            for i, pred in enumerate(predictions)
        ]

        write_submission(
            task=self.current_task,
            predictions_data=predictions_data,
            output_dir=self.hulu_args.output_dir,
        )
