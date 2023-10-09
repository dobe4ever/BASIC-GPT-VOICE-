import json
import os
import openai
from functions import functions
from utils import load_json, save_json, append_message, set_gpt_model, clear_conversation, custom_instructions

# Define the OpenAI key from the environment variable
openai.api_key = os.environ['OPENAI_API_KEY']


def call_function(function_call):
    if function_call["name"] == "set_custom_instructions":
        args = json.loads(function_call["arguments"])
        args = args.get("instructions")
        conversation = load_json("conversation.json")
        conversation = conversation[0]
        conversation[0]["content"] = args
        save_json(conversation, "conversation.json")
        return "Custom instructions set successfully!"


def run_conversation(user_message):
    append_message("user", user_message)
    conversation = load_json("conversation.json")
    settings = load_json("settings.json")
    
    response = openai.ChatCompletion.create(
        model=settings["model"],
        messages=[conversation[0]] + conversation[-5:],
        functions=functions,
        function_call="auto"
    )
    response = response["choices"][0]["message"]
    # Step 2: check if GPT wanted to call a function
    if response.get("function_call"):
        return call_function(response["function_call"])
    else:
        append_message("assistant", response["content"])
        return response["content"]
    

def transcribe_voice(voice):
    transcript = openai.Audio.transcribe(
        "whisper-1",
        voice, 
        temperature = 0.0,
    )
    return transcript['text']





