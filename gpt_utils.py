import json
import os
import openai
from utils import load_json, save_json, append_message, calculate_cost, update_balance, userdata, load_userdata, context

# Define the OpenAI key from the environment variable
openai.api_key = os.environ['OPENAI_API_KEY']


def run_conversation(userid, user_message):
    append_message(userid, "user", user_message)
    response = openai.ChatCompletion.create(
        model=userdata(userid, 'model'),
        messages=context(userid, window=5),
        max_tokens=1024,
        user=str(userid)
    )
    update_balance(userid, calculate_cost(response))
    
    response = response["choices"][0]["message"]["content"]
    append_message(userid, "assistant", response)
    return response

def transcribe_voice(voice):
    transcript = openai.Audio.transcribe(
        "whisper-1",
        voice, 
        temperature = 0.0,
    )
    return transcript['text']





