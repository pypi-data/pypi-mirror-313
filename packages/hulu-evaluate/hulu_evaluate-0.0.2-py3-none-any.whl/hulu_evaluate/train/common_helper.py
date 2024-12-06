import json
import os
from pathlib import Path


def reach_data(task):
    current_dir = Path(__file__).resolve().parent
    data_path = current_dir.parent / "data_path"

    with open(f"{data_path}/{task}.json", "r", encoding="utf8") as f:
        data = json.load(f)

    return data


def write_submission(task, predictions_data, output_dir):

    os.makedirs(output_dir, exist_ok=True)
    base_filename = f"{task}_predicted_labels.json"
    predictions_path = os.path.join(output_dir, base_filename)

    file_index = 1
    while os.path.exists(predictions_path):
        predictions_path = os.path.join(
            output_dir, f"{task}_predicted_labels_{file_index}.json"
        )
        file_index += 1

    with open(predictions_path, "w", encoding="utf8") as f:
        json.dump(predictions_data, f, indent=4)

    print(f"\n######### Saved predicted labels to {predictions_path} #########\n")
