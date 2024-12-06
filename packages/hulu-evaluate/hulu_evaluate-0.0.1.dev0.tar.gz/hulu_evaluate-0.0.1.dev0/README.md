# HuLU evaluate

`hulu_evaluate` is a library for evaluating and training language models on Hungarian tasks within the HuLU benchmark. It includes support for fine-tuning with LoRA, official evaluation scripts, and provides a leaderboard for benchmarking.

## Features

- **Training on multiple tasks**: Supports tasks like "CoLA", "RTE", "WNLI", "CB", "SST", and more.
- **LoRA (Low-Rank Adaptation)**: Fine-tune models with reduced compute requirements.
- **Official training scripts**: Provided for training and evaluation.
- **HuLU Leaderboard**: Submit your results to the HuLU leaderboard.

## Installation

To install the `hulu_evaluate` library, clone the repository and install dependencies:

```bash
pip install git+https://github.com/yourusername/hulu_evaluate.git
```

## Usage
Command-Line Interface (CLI)
The CLI provides commands for configuration, training, login, and submission.

Setting Up the CLI
The CLI entry point can be called with:

```bash
Copy code
hulu-evaluate <command> [<args>]
```
### Commands include:

config: Get configuration parser for model arguments.
submit: Submit model results to the HuLU leaderboard.
login: Authenticate for submission.
train: Train a model on specified HuLU tasks.
Example: Training and Submitting a Model
Login (for leaderboard submissions):

```bash
hulu-evaluate login --config_file <path_to_config.yaml>
```

## Train a Model: Train on HuLU tasks using the train command:

```bash
hulu-evaluate train --model_name <MODEL_NAME> --output_dir <OUTPUT_DIR> --train_epochs 6 --train_batch 8
```

## Submit Results: Submit the results from training to the HuLU leaderboard:

```bash
hulu-evaluate submit <path_to_result_file>
```
## Programmatic Usage
You can also integrate hulu_evaluate functionality directly in Python scripts.

Training
```python
from hulu_evaluate.commands.train import train_command_parser
from hulu_evaluate.hulu_arguments.train_arguments import HuluArgument

# Define training arguments
arguments = HuluArgument(
    model_name="my_model",
    train_epochs=6,
    tasks=["cola", "rte"],
    use_lora=True
)

# Train the model
HuluMain(arguments)
```
## Submission
```python
from hulu_evaluate.commands.submit import submit_command

# Define submission arguments
result_file = "path/to/result_file.json"
submit_command(result_file)
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
### Submit Command
submit - Submits model evaluation results to the HuLU leaderboard.

```bash
hulu-evaluate submit <path_to_result_file>
```
result_file: Path to the result file (JSON format).
### Login Command
login - Authenticates for leaderboard submission.

```bash
hulu-evaluate login --config_file <config_file_path>
```
### Contributing
Contributions are welcome! Please submit issues or pull requests to improve hulu_evaluate.

### License
This project is licensed under the Apache License.