# HuLU evaluate

`hulu_evaluate` is a library for evaluating and training language models on Hungarian tasks within the HuLU benchmark. It includes support for fine-tuning with LoRA, official evaluation scripts, and provides a leaderboard for benchmarking.

## Features

- **Training on multiple tasks**: Supports tasks like "CoLA", "RTE", "WNLI", "CB", "SST", and "COPA".
- **LoRA (Low-Rank Adaptation)**: Fine-tune models with reduced compute requirements.
- **Official training scripts**: Provided for training and evaluation.
- **HuLU Leaderboard**: Submit your results to the HuLU leaderboard.

## Installation

To install the `hulu_evaluate` library, clone the repository and install dependencies:

```bash
pip install git+https://git.nlp.nytud.hu/DLT/HuLU-evaluate.git
```

## Usage
Command-Line Interface (CLI)
The CLI provides commands for configuration, training, and submission.

Setting Up the CLI
The CLI entry point can be called with:

```bash
hulu-evaluate <command> [<args>]
```
### Commands include:

## Train a Model: Train on HuLU tasks using the train command:

```bash
hulu-evaluate train --model_name <MODEL_NAME> --output_dir <OUTPUT_DIR> --train_epochs 6 --train_batch 8
```

You can submit your results on the hulu.nytud.hu webpage. The results are created by default in the "HuluFinetune" directory. 

## Programmatic Usage
You can also integrate hulu_evaluate functionality directly in Python scripts.

Training
```python
from hulu_evaluate.train.hulu_main import HuluMain
from hulu_evaluate.hulu_arguments.train_arguments import HuluArgument

# Define training arguments
arguments = HuluArgument(
    model_name="my_model",
    train_epochs=6,
    tasks=["cola", "rte"],
)

# Train the model
HuluMain(arguments)
```

## Command Reference
### Training Command
train - Trains a model on HuLU tasks with specified parameters.

```bash
hulu-evaluate train --model_name <MODEL_NAME> --output_dir <OUTPUT_DIR> --train_epochs <EPOCHS>
--model_name: Name of the model to train.
--train_epochs: Number of epochs.
--use_lora: Enable LoRA fine-tuning (optional).
```

### Contributing
Contributions are welcome! Please submit issues or pull requests to improve hulu_evaluate.

### License
This project is licensed under the Apache License.