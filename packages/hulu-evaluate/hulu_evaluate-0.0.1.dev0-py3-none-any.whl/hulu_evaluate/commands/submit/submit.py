from hulu_evaluate.commands.config.config_utils import SubcommandHelpFormatter
import torch
from pydantic import BaseModel
import json
import requests

class HuluSubmission(BaseModel):
    team_name: str
    model_name: str
    url: str
    contact: str
    train_epochs: int
    train_batch: int
    train_lr: float
    train_warmup: int
    train_steps: int
    train_maxlen: int
    train_seed: int
    train_loss: str
    gpu_memory: int
    gpu_count: int
    fine_tune_mode: str
    quantized_bits: int
    model_parameters: int

    model_config = {"protected_namespaces": ()}
    model_name = {"protected_namespaces": ()}

def collect_device_info():
    device = torch.cuda.current_device()
    device_name = torch.cuda.get_device_name(device=device)
    gpu_memory = torch.cuda.get_device_properties(device=device).total_memory
    gpu_count = torch.cuda.device_count()
    return  device_name, gpu_memory, gpu_count

def collect_model_info_from_result_file(result_file, **kwargs):
    with open(result_file, 'r') as f:
        json_data = json.load(f)
    
    return HuluSubmission(**json_data)

def collect_team_info():
    team_name = input("Enter your team name: ")
    model_name = input("Enter your model name: ")
    url = input("Enter the URL of your model: ")
    contact = input("Enter your email address: ")
    return team_name, model_name, url, contact

def submit(submission):
    try:
        response = requests.post("https://hulu.nytud.hu/submit-lib", json=submission.dict())
        response.raise_for_status()
        print("Submission successful.")
    except requests.exceptions.HTTPError as e:
        print(f"Submission failed: {e}")
        


def submit_command(args):
    print(f"Submitting results from file: {args.result_file}")
    print("Please enter the following information:")
    team_name, model_name, url, contact = collect_team_info()
    device_name, gpu_memory, gpu_count = collect_device_info()
    submission = collect_model_info_from_result_file(args.result_file, team_name=team_name, model_name=model_name, url=url, contact=contact, gpu_memory=gpu_memory, gpu_count=gpu_count)
    print(submission)
    submit(submission)
    



def submit_command_parser(subparsers):
    submit_parser = subparsers.add_parser("submit", help="Submit results to HuLU", formatter_class=SubcommandHelpFormatter)
    submit_parser.add_argument("result_file", help="Path to the result file")
    submit_parser.set_defaults(func=submit_command)
