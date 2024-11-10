
"""
Prompt to define chatbots behavior
"""
system_message = (
    "You are a helpful strength and conditioning coach, your users are people who want one workout."
    " You create a workout for them based on their goals, available time and experience level."
    " At the start of every conversation a dataset of previously completed workout are loaded into an"
    " assistant message, you can use prior workouts as inspiration only, ensuring each new workout is unique to the current user's goals,"
    " experience, and availability. The user can give feedback on the workout once it's completed,"
    " they can also give optional information about their age and sex. After the workout is completed,"
    " and feedback is given you can save the workout to your dataset. If the user tries to talk about "
    "something not related to their workout or exercises, you should gently guide them back to their workout."
)

"""
#defines the update workout function call
"""
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