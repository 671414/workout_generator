#Updates the csv file with a new workout
#Code from https://www.geeksforgeeks.org/how-to-append-a-new-row-to-an-existing-csv-file/
import asyncio
import json
import pandas as pd
from datasets import Dataset, load_dataset
from huggingface_hub import HfApi

api = HfApi()
"""
parses tool_call message to correct format
@param tool_call message
@return tool_call message content 
"""
def tool_call_to_workout_parse(message):
    tool_call_data = message.choices[0].message.tool_calls[0].function.arguments
    message_data = json.loads(tool_call_data)["message"]
    return message_data

"""
Saves message in correct format in our dataset
@param tool_call message
"""
def save_to_hub(message):
    dataset = update_dataset(message)
    dataset.push_to_hub("KasparER/completed_workouts", commit_message="Updating workouts")
"""
Loads our dataset from huggingface.
@return dataset as pandas dataframe
"""
def load_dataset_from_hub():
    ds = load_dataset("KasparER/completed_workouts", split="train")
    df = pd.DataFrame(ds)
    return df
"""
Adds the new workout to our dataset, and transforms it into correct dataset format
@param message
@return dataset as huggingface dataset
"""
def update_dataset(message):
    #only the csv
    dataset = load_dataset_from_hub()
    #Parsing the message to correct format
    new_row = tool_call_to_workout_parse(message)
    #Changing it to fit a panda
    dataset_data = pd.DataFrame([new_row])
    #adding it to the previous one
    updated_dataset = pd.concat([dataset, dataset_data], ignore_index=True)
    #formatting it into a dataset that can be pushed.
    updated_hf_dataset = Dataset.from_pandas(updated_dataset)
    return updated_hf_dataset
