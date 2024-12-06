import json
import requests
from datasets import Dataset
from transformers import AutoTokenizer
from hulu_evaluate.hulu_arguments import HuluArgument
from hulu_evaluate.train.common_helper import reach_data
from hulu_evaluate.train.constants import SST_LABELS, CB_LABELS


class HuluPreprocessPipeLine:

    def __init__(self, hulu_args: HuluArgument, current_task: str):
        self.hulu_args = hulu_args
        self.current_task = current_task

        train_dataset, dev_dataset, test_dataset = self.select_dataset()

        (
            self.tokenized_train_dataset,
            self.tokenized_dev_dataset,
            self.tokenized_test_dataset,
        ) = self.tokenize_different_datasets(train_dataset, dev_dataset, test_dataset)

    def _fetch_data(self, url):
        response = requests.get(url)
        if self.current_task == "cb":
            return json.loads(response.content.decode("utf-8-sig"))
        return response.json()

    def select_dataset(self):

        data=reach_data(self.current_task)

        dev_dataset_link = data.get("dev_dataset_url")
        test_dataset_link = data.get("test_dataset_url")
        train_dataset_link = data.get("train_dataset_url")

        train_data = self._fetch_data(train_dataset_link)
        dev_data = self._fetch_data(dev_dataset_link)
        test_data = self._fetch_data(test_dataset_link)

        if self.current_task in ["cola", "rte", "wnli"]:
            dev_data = [{**item, "label": int(item["label"])} for item in dev_data]
            train_data = [{**item, "label": int(item["label"])} for item in train_data]

        elif self.current_task == "sst":
            dev_data = [
                {**item, "label": SST_LABELS[item["label"]]} for item in dev_data
            ]
            train_data = [
                {**item, "label": SST_LABELS[item["label"]]} for item in train_data
            ]

        elif self.current_task == "cb":
            dev_data = [
                {**item, "label": CB_LABELS[item["label"]]} for item in dev_data
            ]
            train_data = [
                {**item, "label": CB_LABELS[item["label"]]} for item in train_data
            ]

        train_dataset = Dataset.from_list(train_data)
        dev_dataset = Dataset.from_list(dev_data)
        test_dataset = Dataset.from_list(test_data)

        return train_dataset, dev_dataset, test_dataset

    def tokenize_different_datasets(self, train_dataset, dev_dataset, test_dataset):

        tokenized_train_dataset = None
        tokenized_dev_dataset = None
        tokenized_test_dataset = None

        try:
            tokenizer = AutoTokenizer.from_pretrained(self.hulu_args.tokenizer_name)
            if tokenizer.pad_token is None:
                tokenizer.pad_token=tokenizer.eos_token
        except Exception as e:

            print(f"Error loading tokenizer: {e}")
            raise ValueError(f"Invalid tokenizer name: {self.hulu_args.tokenizer_name}")

        if self.current_task == "cola" or self.current_task == "sst":
            tokenized_train_dataset = train_dataset.map(
                lambda examples: tokenizer(
                    examples["Sent"],
                    truncation=True,
                    padding="max_length",
                    max_length=self.hulu_args.train_maxlen,
                    add_special_tokens=True,
                ),
                batched=True,
                remove_columns=["id", "Sent"],
            )
            tokenized_dev_dataset = dev_dataset.map(
                lambda examples: tokenizer(
                    examples["Sent"],
                    truncation=True,
                    padding="max_length",
                    max_length=self.hulu_args.train_maxlen,
                    add_special_tokens=True,
                ),
                batched=True,
                remove_columns=["id", "Sent"],
            )
            tokenized_test_dataset = test_dataset.map(
                lambda examples: tokenizer(
                    examples["Sent"],
                    truncation=True,
                    padding="max_length",
                    max_length=self.hulu_args.train_maxlen,
                    add_special_tokens=True,
                ),
                batched=True,
                remove_columns=["id", "Sent"],
            )

        elif self.current_task == "wnli":
            tokenized_train_dataset = train_dataset.map(
                lambda examples: tokenizer(
                    examples["sentence1"],
                    examples["sentence2"],
                    truncation=True,
                    max_length=self.hulu_args.train_maxlen,
                    padding="max_length",
                ),
                batched=True,
                remove_columns=["id", "sentence1", "sentence2", "orig_id"],
            )
            tokenized_dev_dataset = dev_dataset.map(
                lambda examples: tokenizer(
                    examples["sentence1"],
                    examples["sentence2"],
                    truncation=True,
                    max_length=self.hulu_args.train_maxlen,
                    padding="max_length",
                ),
                batched=True,
                remove_columns=["id", "sentence1", "sentence1", "orig_id"],
            )
            tokenized_test_dataset = test_dataset.map(
                lambda examples: tokenizer(
                    examples["sentence1"],
                    examples["sentence2"],
                    truncation=True,
                    max_length=self.hulu_args.train_maxlen,
                    padding="max_length",
                ),
                batched=True,
                remove_columns=["id", "sentence1", "sentence1", "orig_id", "label"],
            )
            

        elif self.current_task == "rte":
            tokenized_train_dataset = train_dataset.map(
                lambda examples: tokenizer(
                    examples["premise"],
                    examples["hypothesis"],
                    truncation=True,
                    max_length=self.hulu_args.train_maxlen,
                    padding="max_length",
                ),
                batched=True,
                remove_columns=["id", "premise", "hypothesis"],
            )
            tokenized_dev_dataset = dev_dataset.map(
                lambda examples: tokenizer(
                    examples["premise"],
                    examples["hypothesis"],
                    truncation=True,
                    max_length=self.hulu_args.train_maxlen,
                    padding="max_length",
                ),
                batched=True,
                remove_columns=["id", "premise", "hypothesis"],
            )
            tokenized_test_dataset = test_dataset.map(
                lambda examples: tokenizer(
                    examples["premise"],
                    examples["hypothesis"],
                    truncation=True,
                    max_length=self.hulu_args.train_maxlen,
                    padding="max_length",
                ),
                batched=True,
                remove_columns=["id", "premise", "hypothesis"],
            )

        elif self.current_task == "cb":
            tokenized_train_dataset = train_dataset.map(
                lambda examples: tokenizer(
                    examples["premise"],
                    examples["hypothesis"],
                    truncation=True,
                    padding="longest",
                ),
                batched=True,
                remove_columns=["id", "premise", "hypothesis"],
            )
            tokenized_dev_dataset = dev_dataset.map(
                lambda examples: tokenizer(
                    examples["premise"],
                    examples["hypothesis"],
                    truncation=True,
                    padding="longest",
                ),
                batched=True,
                remove_columns=["id", "premise", "hypothesis"],
            )

            tokenized_test_dataset = test_dataset.map(
                lambda examples: tokenizer(
                    examples["premise"],
                    examples["hypothesis"],
                    truncation=True,
                    padding="longest",
                ),
                batched=True,
                remove_columns=["id", "premise", "hypothesis"],
            )

        return tokenized_train_dataset, tokenized_dev_dataset, tokenized_test_dataset
