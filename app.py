import utils
import gradio as gr
from openai import OpenAI
import os
import chatbot_tools_and_messages
from utils import update_dataset, save_to_hub

api_key=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

title = 'Workout Generator'
"""
Our chatbot, with saved chat history for every new workout
@param message
@param history 
"""
async def chatbot_response(message, history=[]):
    #Conversation history
    history.append({"role": "system", "content": chatbot_tools_and_messages.system_message })
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": utils.load_dataset_from_hub().to_string()})
    print(utils.load_dataset_from_hub().to_string())
    #Generate response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history,
        temperature=1,
        tools=chatbot_tools_and_messages.tools,

    )

    #Checks if a tool call has been done, in our case, saved to file
    if response.choices[0].finish_reason == "tool_calls":
        #updating the file
        save_to_hub(response)
        return "Workout saved! Go get some rest, and feel free to use me for your next workout."

    # If no function call, return the chatbot's generated message
    workout_generator_reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": workout_generator_reply})
    return workout_generator_reply


gr.ChatInterface(chatbot_response, type="messages",
                 textbox=gr.Textbox(placeholder="Let me help you generate a workout", container=False),
                 title=title,
                 ).launch()

