from argparse import Namespace

from hulu_evaluate.commands.utils import SubcommandHelpFormatter
from hulu_evaluate.hulu_arguments.train_arguments import HuluArgument
from hulu_evaluate.train.hulu_main import HuluMain


def train_command(args: Namespace):
    print("Training model on tasks of HuLu")
    if args.config_file:
        arguments = HuluArgument.from_json(args.config_file)
    else:
        # Pass arguments directly to HuluArgument
        arguments = HuluArgument(
            output_dir=args.output_dir,
            model_name=args.model_name,
            tokenizer_name=args.tokenizer_name,
            train_epochs=args.train_epochs,
            train_batch=args.train_batch,
            train_lr=args.train_lr,
            train_warmup=args.train_warmup,
            train_maxlen=args.train_maxlen,
            train_seed=args.train_seed,
            precision=args.precision,
            use_lora=args.use_lora,
            lora_r=args.lora_r,
            lora_alpha=args.lora_alpha,
            lora_dropout=args.lora_dropout,
            tasks=args.tasks,
        )
    HuluMain(arguments)


def train_command_parser(subparsers):
    train_parser = subparsers.add_parser(
        "train",
        help="Train model on tasks of HuLU",
        formatter_class=SubcommandHelpFormatter,
    )

    train_parser.add_argument(
        "--config_file", type=str, help="Path to config JSON file"
    )
    train_parser.add_argument(
        "--output_dir", type=str, default="HuluFinetune", help="Output directory"
    )
    train_parser.add_argument(
        "--model_name", type=str, required=True, help="Model name"
    )
    train_parser.add_argument(
        "--tokenizer_name", type=str, help="Tokenizer name (defaults to model_name)"
    )
    train_parser.add_argument(
        "--train_epochs", type=int, default=6, help="Number of training epochs"
    )
    train_parser.add_argument(
        "--train_batch", type=int, default=8, help="Training batch size"
    )
    train_parser.add_argument(
        "--train_lr", type=float, default=2e-05, help="Learning rate"
    )
    train_parser.add_argument(
        "--train_warmup", type=int, default=0, help="Warmup steps"
    )
    train_parser.add_argument(
        "--train_maxlen", type=int, default=256, help="Max sequence length"
    )
    train_parser.add_argument("--train_seed", type=int, default=42, help="Random seed")
    train_parser.add_argument(
        "--precision", type=str, default="fp32", help="Precision (e.g., fp16 or fp32)"
    )
    train_parser.add_argument(
        "--use_lora", action="store_true", help="Use LoRA for training", default=False
    )
    train_parser.add_argument("--lora_r", type=int, default=8, help="LoRA r parameter")
    train_parser.add_argument(
        "--lora_alpha", type=int, default=16, help="LoRA alpha parameter"
    )
    train_parser.add_argument(
        "--lora_dropout", type=float, default=0.1, help="LoRA dropout rate"
    )
    train_parser.add_argument(
        "--tasks",
        type=str,
        nargs="+",
        default=["cola", "rte", "wnli", "cb", "sst"],
        help="List of tasks to train on",
    )

    train_parser.set_defaults(func=train_command)
