import torch
from transformers import AutoTokenizer
from datasets import load_dataset
from torch.utils.data import DataLoader
from hulu_evaluate.hulu_arguments.train_arguments import HuluArgument
from hulu_evaluate.train.common_helper import reach_data
from hulu_evaluate.train.constants import CONJUNCTIONS


class CopaPreprocessPipeline:
    def __init__(self, hulu_args: HuluArgument):
        self.hulu_args = hulu_args
        self.tokenizer = AutoTokenizer.from_pretrained(self.hulu_args.tokenizer_name)

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        (
            self.tokenized_train_loader,
            self.tokenized_dev_loader,
            self.tokenized_test_loader,
        ) = self.load_and_preprocesss()

    def preprocess_example(self, premise, choices, question):
        input_strings = [
            f"{premise} {CONJUNCTIONS[question]} {choice}" for choice in choices
        ]
        tokenized_choices = [
            self.tokenizer(
                input_str,
                truncation=True,
                max_length=self.hulu_args.train_maxlen,
                padding="max_length",
            )
            for input_str in input_strings
        ]
        input_ids = torch.tensor([x["input_ids"] for x in tokenized_choices])
        attention_mask = torch.tensor([x["attention_mask"] for x in tokenized_choices])

        return input_ids, attention_mask

    def preprocess_data(self, example, is_test=False):
        input_ids, attention_mask = self.preprocess_example(
            example["premise"],
            [example["choice1"], example["choice2"]],
            example["question"],
        )

        if is_test:
            return {
                "input_ids": torch.tensor(input_ids),
                "attention_mask": torch.tensor(attention_mask),
            }
        else:
            return {
                "input_ids": torch.tensor(input_ids),
                "attention_mask": torch.tensor(attention_mask),
                "label": torch.tensor(int(example["label"]) - 1, dtype=torch.long),
            }

    def collate_fn(self, batch):

        for item in batch:
            item["input_ids"] = torch.tensor(item["input_ids"], dtype=torch.long)
            item["attention_mask"] = torch.tensor(
                item["attention_mask"], dtype=torch.long
            )
            if "label" in item:
                item["label"] = torch.tensor(item["label"], dtype=torch.long)

        input_ids = torch.stack([item["input_ids"] for item in batch])
        attention_mask = torch.stack([item["attention_mask"] for item in batch])
        labels = (
            torch.stack([item["label"] for item in batch])
            if "label" in batch[0]
            else None
        )
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "label": labels,
        }

    def load_and_preprocesss(self):

        data=reach_data("copa")

        dev_data = load_dataset("json", data_files=str(data.get("dev_dataset_url")))["train"]
        train_data = load_dataset("json", data_files=str(data.get("train_dataset_url")))["train"]
        test_data = load_dataset("json", data_files=str(data.get("test_dataset_url")))["train"]

        dev_data = dev_data.map(lambda x: self.preprocess_data(x, is_test=False))
        train_data = train_data.map(lambda x: self.preprocess_data(x, is_test=False))
        test_data = test_data.map(lambda x: self.preprocess_data(x, is_test=True))

        train_loader = DataLoader(
            train_data,
            batch_size=self.hulu_args.train_batch,
            shuffle=True,
            collate_fn=self.collate_fn,
        )
        dev_loader = DataLoader(
            dev_data,
            batch_size=self.hulu_args.train_batch,
            shuffle=False,
            collate_fn=self.collate_fn,
        )
        test_loader = DataLoader(
            test_data,
            batch_size=self.hulu_args.train_batch,
            shuffle=False,
            collate_fn=self.collate_fn,
        )

        return train_loader, dev_loader, test_loader
