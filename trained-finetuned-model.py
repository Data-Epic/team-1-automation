import os
from dotenv import load_dotenv
import cohere


# Load environment variables from .env file
load_dotenv()

# Initialize the Cohere client
API_KEY = os.getenv('COHERE_API_KEY')
if API_KEY is None:
    raise ValueError("Please set the COHERE_API_KEY environment variable.")
co = cohere.ClientV2(API_KEY)

# create dataset
single_label_dataset = co.datasets.create(
    name="single-label-dataset",
    data=open("sentiment-classification.jsonl", "rb"),
    type="single-label-classification-finetune-input",
)

print(co.wait(single_label_dataset).dataset.validation_status)

# start the fine-tune job using this dataset
from cohere.finetuning.finetuning import (
    BaseModel,
    FinetunedModel,
    Settings,
)

single_label_finetune = co.finetuning.create_finetuned_model(
    request=FinetunedModel(
        name="single-label-finetune",
        settings=Settings(
            base_model=BaseModel(
                base_type="BASE_TYPE_CLASSIFICATION",
            ),
            dataset_id=single_label_dataset.id,
        ),
    ),
)

print(
    f"fine-tune ID: {single_label_finetune.finetuned_model.id}, fine-tune status: {single_label_finetune.finetuned_model.status}"
)
