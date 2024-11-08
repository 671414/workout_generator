#Updates the csv file with a new workout
#Code from https://www.geeksforgeeks.org/how-to-append-a-new-row-to-an-existing-csv-file/
import asyncio
import json
import pandas as pd
from datasets import Dataset
from huggingface_hub import HfApi

api = HfApi()

#parses the tool message to correct format
def tool_call_to_workout_parse(message):
    tool_call_data = message.choices[0].message.tool_calls[0].function.arguments
    message_data = json.loads(tool_call_data)["message"]
    return message_data

#Pushes the completed workout to our huggingface dataset
def save_to_hub(message):
    print("Saving workout")
    dataset = update_dataset(message)
    dataset.push_to_hub("KasparER/completed_workouts")

#Loads our dataset from huggingface.
def load_dataset_from_hub():
    df = pd.read_csv("hf://datasets/KasparER/completed_workouts/completed_workouts.csv")
    #df = load_dataset("KasparER/completed_workouts")
    return df

#Adds the new workout to our dataset, and transforms it into correct dataset format
def update_dataset(message):
    dataset = load_dataset_from_hub()
    #new_row = pd.DataFrame(tool_call_to_workout_parse(message))
    new_row = tool_call_to_workout_parse(message)
    dataset_data = pd.DataFrame([new_row])
    updated_dataset = pd.concat([dataset, dataset_data], ignore_index=True, )
    updated_hf_dataset = Dataset.from_pandas(updated_dataset)
    return updated_hf_dataset
