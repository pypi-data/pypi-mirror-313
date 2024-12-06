from pydantic import BaseModel, model_validator, field_validator
import json
from typing import List, Optional


class HuluArgument(BaseModel):
    output_dir: str = "HuluFinetune"
    model_name: str
    tokenizer_name: Optional[str] = None
    train_epochs: int = 6
    train_batch: int = 8
    train_lr: float = 2e-05
    train_warmup: int = 0
    train_maxlen: int = 256
    train_seed: int = 42
    precision: str = "fp32"
    use_lora: bool = False
    lora_r: int = 8
    lora_alpha: int = 16
    lora_dropout: float = 0.1
    tasks: List[str] = ["cola", "rte", "wnli", "cb", "sst"]

    model_config = {"protected_namespaces": ()}

    @model_validator(mode="before")
    def set_tokenizer_name(cls, values):
        if values.get("tokenizer_name") is None:
            values["tokenizer_name"] = values["model_name"]
        return values

    @field_validator("tasks", mode="before")
    def validate_tasks(cls, v):
        allowed_tasks = {"cola", "rte", "wnli", "cb", "sst", "copa"}
        invalid_tasks = [task for task in v if task not in allowed_tasks]
        if invalid_tasks:
            raise ValueError(
                f"Invalid tasks found: {invalid_tasks}. Allowed tasks are: {allowed_tasks}"
            )
        return v

    @classmethod
    def from_json(cls, json_path: str):
        with open(json_path, "r") as file:
            data = json.load(file)
        return cls(**data)
