#Updates the csv file with a new workout
#Code from https://www.geeksforgeeks.org/how-to-append-a-new-row-to-an-existing-csv-file/
import asyncio
import json
import os
from csv import DictWriter
import datasets
import pandas as pd
from datasets import Dataset
from pandas.errors import EmptyDataError
from huggingface_hub import HfApi

api = HfApi()
#Updates the dataset, will be changed to fit dataset stored on huggingface
def write_to_csv(message):
    #logging.info("update_workout_csv called with message: %s", message)
    field_names = ['AGE', 'SEX', 'EXPERIENCE_LEVEL', 'GOAL', 'WORKOUT_TYPE', 'EXERCISES', 'SETS', 'REPETITIONS', 'FEEDBACK']

    # Check if file exists to add headers only once
    file_exists = os.path.isfile('completed_workouts.csv')

    with open('completed_workouts.csv', 'a', newline='') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)

        # Write header only if file is being created
        if not file_exists:
            dictwriter_object.writeheader()

        dictwriter_object.writerow(message)
        f_object.close()
#async wrapper need previously
async def update_workout_csv_async(message):
    message_data = tool_call_to_workout_parse(message)
    await asyncio.to_thread(update_dataset, message_data)
    return True

#Reads the dataset from huggingface
def read_dataset():
    try:
        df = pd.read_csv("completed_workouts.csv", encoding='utf-8')
        return df.to_string()
    except EmptyDataError:
        return "No previous workouts recorded"

#parses the tool message from gpt to dict format
def tool_call_to_workout_parse(message):
    tool_call_data = message.choices[0].message.tool_calls[0].function.arguments
    message_data = json.loads(tool_call_data)["message"]
    return message_data

def save_to_hub(message):
    dataset = update_dataset(message)
    dataset.push_to_hub("KasparER/completed_workouts")

def load_dataset():
    dataset = load_dataset("KasparER/completed_workouts")
    return dataset.to_pandas()

def update_dataset(message):
    dataset = load_dataset()
    new_row = pd.DataFrame(tool_call_to_workout_parse(message))
    dataset = pd.concat([dataset, new_row])
    updated_dataset = Dataset.from_pandas(dataset)
    return updated_dataset
