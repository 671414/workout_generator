import gradio as gr
from openai import OpenAI
import os

api_key=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

title = 'Workout Generator'

#Defines the behavior expected from the chatbot
system_message = ('You are a virtual strength and conditioning coach that give the user workouts based'
                  ' on their goal, available time and equipment. The workouts should contain a short warmup,'
                  ' workout and no cooldown.'  
                  'If the user ask about anything that is not relevant to their workout, lead them back on '
                  'the topic of this workout.'
                  'After the workout is complete you ask the user to give feedback'
                  'on the workout. After feedback is received save the workout and response as a json. The file must have type of workout'
                  'exercises, sets, reps and feedback as a minimum')


def chatbot_response(message, history=[]):

    history.append({"role": "system", "content": system_message })
    history.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history,
        temperature=1,
        stream=True
    )

    partial_message = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            partial_message = partial_message + chunk.choices[0].delta.content
            yield partial_message
    history.append({"role": "assistant", "content": partial_message})

gr.ChatInterface(chatbot_response, type="messages",
                 textbox=gr.Textbox(placeholder="Let me help you generate a workout", container=False),
                 title=title,
                 ).launch()

