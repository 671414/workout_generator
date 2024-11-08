#Updates the csv file with a new workout
#Code from https://www.geeksforgeeks.org/how-to-append-a-new-row-to-an-existing-csv-file/
import asyncio
import json
import os
from csv import DictWriter

import pandas as pd
from pandas.errors import EmptyDataError


def update_workout_csv(message):
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

async def update_workout_csv_async(message):
    message_data = tool_call_to_workout_parse(message)
    await asyncio.to_thread(update_workout_csv, message_data)
    return True

def read_previous_workouts():
    try:
        df = pd.read_csv("completed_workouts.csv", encoding='utf-8')
        return df.to_string()
    except EmptyDataError:
        return "No previous workouts recorded"

def tool_call_to_workout_parse(message):
    tool_call_data = message.choices[0].message.tool_calls[0].function.arguments
    message_data = json.loads(tool_call_data)["message"]
    return message_data
