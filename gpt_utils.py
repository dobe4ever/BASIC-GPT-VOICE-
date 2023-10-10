import json
import os
import openai
from functions import functions
# from classes import UserData
from utils import load_json, save_json, append_message, set_gpt_model, clear_conversation, custom_instructions, calculate_token_cost, update_balance

# Define the OpenAI key from the environment variable
openai.api_key = os.environ['OPENAI_API_KEY']

# # Example usage:
# user_id = 548104065
# user = UserData(user_id)
# print(user.get_system_message())  # Access system message content
# print(user.get_recent_messages(2))  # Access the last 2 messages
# user.add_message(role="user", content="Hello!")
# user.add_message("assistant", "Hi there! How can I assist you today?")
# print(user.get_user_data("username"))  # Access username
# user.update_user_data("usd_credit", 10.0)  # Update USD credit


def call_function(userid, function_call):
    if function_call['name'] == "set_custom_instructions":
        args = json.loads(function_call['arguments'])
        args = args.get('instructions')
        userdata = load_json(f"persistent/users/{userid}.json")
        userdata = userdata[1]
        userdata['content'] = args
        save_json(userdata, f"persistent/users/{userid}.json")
        return "Custom instructions set successfully!"
    else:
        return "Something went wrong..."    


def run_conversation(userid, user_message):
    userdata = append_message(userid, "user", user_message)
    context = [userdata[1]] + userdata[2:][-5:]
    response = openai.ChatCompletion.create(
        model=userdata[0]["model"],
        messages=context,
        functions=functions,
        function_call="auto"
    )
    cost = calculate_token_cost(response)
    
    update_balance(userid, cost)
    
    response = response["choices"][0]["message"]
    # Step 2: check if GPT wanted to call a function
    if response.get("function_call"):
        return call_function(userid, response["function_call"])
    else:
        append_message(userid, "assistant", response["content"])
        return response["content"]
    

def transcribe_voice(voice):
    transcript = openai.Audio.transcribe(
        "whisper-1",
        voice, 
        temperature = 0.0,
    )
    return transcript['text']





