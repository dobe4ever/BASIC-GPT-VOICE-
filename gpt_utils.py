import json
import os
from flask.scaffold import _matching_loader_thinks_module_is_package
import openai
from utils import load_json, save_json, append_message, calculate_cost, update_balance, userdata, load_userdata, context

# Define the OpenAI key from the environment variable
openai.api_key = os.environ['OPENAI_API_KEY']

def run_conversation(userid, user_message):

    print("running cnversation")
    
    append_message(userid, "user", user_message)
    model = userdata(userid, 'model')
    print(model)
    messages=context(userid, window=20)
    print(f"Mwssages: {messages}")
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=1024,
        user=str(userid)
    )
    cost = calculate_cost(response)
    print(f"cost: {cost}")
    update_balance(userid, cost)
    #print("")
    
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





