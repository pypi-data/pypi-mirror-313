from hulu_evaluate.hulu_arguments.train_arguments import HuluArgument
from hulu_evaluate.train.preprocess import HuluPreprocessPipeLine
from hulu_evaluate.train.train import HuluTrainPipeline
from hulu_evaluate.train.train_copa import CopaTrainPipeline
from hulu_evaluate.train.preprocess_copa import CopaPreprocessPipeline

class HuluMain:
    def __init__(self, hulu_args: HuluArgument):

        self.hulu_args = hulu_args

        for task in self.hulu_args.tasks:
            if task != "copa":
                preprocessing = HuluPreprocessPipeLine(
                    hulu_args=self.hulu_args, current_task=task
                )
                training_pipeline = HuluTrainPipeline(
                    hulu_args=self.hulu_args, current_task=task
                )
                training_pipeline.set_tokenized_datasets(
                    tokenized_train_dataset=preprocessing.tokenized_train_dataset,
                    tokenized_dev_dataset=preprocessing.tokenized_dev_dataset,
                    tokenized_test_dataset=preprocessing.tokenized_test_dataset,
                )

            else:
                preprocessing = CopaPreprocessPipeline(hulu_args=self.hulu_args)
                training_pipeline = CopaTrainPipeline(hulu_args=self.hulu_args)
                training_pipeline.set_tokenized_datasets(
                    train_loader=preprocessing.tokenized_train_loader,
                    dev_loader=preprocessing.tokenized_dev_loader,
                    test_loader=preprocessing.tokenized_test_loader,
                )

            trained_model = training_pipeline.training()
            training_pipeline.create_submission(trained_model)


#An example:
"""
example_args = HuluArgument(
    model_name="SZTAKI-HLT/hubert-base-cc",
    output_dir="my_hulu_output",
    train_epochs=1,
    train_batch=30,
    train_lr=0.001,
    train_maxlen=256,
    use_lora=False,
    tasks=[
        "wnli",
        "sst",
        "cb"
    ],
)

if __name__ == "__main__":
    HuluMain(example_args)
"""

