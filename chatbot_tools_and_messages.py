system_message = (
    "You are a virtual strength and conditioning coach that gives users workouts based on their goal, "
    "available time, and equipment. The workouts should contain a short warmup, a workout, and no cooldown. "
    "If the user asks about anything that is not relevant to their workout, steer them back to the workout topic. "
    "After completing the workout, ask the user for feedback, do not tell the user you save the workout for them,"
    " and add the workout and save it workout in a CSV file in this format: "
    "['AGE': 'age', 'SEX': 'sex', 'EXPERIENCE_LEVEL': 'experience level', 'GOAL': 'goal, 'WORKOUT_TYPE': 'workout_type', 'EXERCISES': 'exercises', 'SETS': 'sets', 'REPETITIONS': 'repetitions', 'FEEDBACK': 'feedback']. "
    "AGE and SEX is not necessary if the do not want to give the info."
)

#defines the update workout function call
tools = [
    {
        "type": "function",
        "function": {
            "name": "update_workout_csv_async",
            "description": "Update the workout csv file; call this when a user has given their feedback and you want to save the workout",
            "strict": True,
            "parameters": {
                "type": "object",
                "required": ["message"],
                "properties": {
                    "message": {
                        "type": "object",
                        "description": "A dictionary containing details about the workout",
                        "properties": {
                            "AGE": {
                                "type": "string",
                                "description": "User's age"
                            },
                            "SEX": {
                                "type": "string",
                                "description": "User's sex"
                            },
                            "EXPERIENCE_LEVEL": {
                                "type": "string",
                                "description": "User's level of experience with workouts"
                            },
                            "GOAL": {
                                "type": "string",
                                "description": "User's fitness goal"
                            },
                            "WORKOUT_TYPE": {
                                "type": "string",
                                "description": "Type of workout performed"
                            },
                            "EXERCISES": {
                                "type": "string",
                                "description": "Exercises included in the workout"
                            },
                            "SETS": {
                                "type": "string",
                                "description": "Number of sets completed"
                            },
                            "REPETITIONS": {
                                "type": "string",
                                "description": "Number of repetitions completed per set"
                            },
                            "FEEDBACK": {
                                "type": "string",
                                "description": "User's feedback on the workout"
                            }
                        },
                        "additionalProperties": False,
                        "required": [
                            "AGE",
                            "SEX",
                            "EXPERIENCE_LEVEL",
                            "GOAL",
                            "WORKOUT_TYPE",
                            "EXERCISES",
                            "SETS",
                            "REPETITIONS",
                            "FEEDBACK"
                        ]
                    }
                },
                "additionalProperties": False
            }
        }
    }
]