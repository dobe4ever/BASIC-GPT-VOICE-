from datetime import datetime
import json
import pytz
from elevenlabs import generate
import openai
from docx import Document
import os

# Define the OpenAI key from the environment variable
openai.api_key = os.environ['OPENAI_API_KEY']

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)
        
def save_json(name, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(name, indent=4, ensure_ascii=False))

def append_message(userid, role, content):
    # Load user data
    userdata = load_json(f"persistent/users/{userid}.json")
    # Append message to the conversation history
    userdata.append({"role": role, "content": content})
    # Save conversation history
    save_json(userdata, f"persistent/users/{userid}.json")
    
    return userdata


# def handle_settings(userid, message):
#     if message == "Use GPT-3.5":
#         return set_gpt_model(userid, "gpt-3.5-turbo")
        
#     if message == "Use GPT-4":
#         return set_gpt_model(userid, "gpt-4")
        
#     if message == "Clear Conversation":
#         return clear_conversation(userid)
        
#     if message == "Custom Instructions":
#         return custom_instructions(userid)
        
#     else: pass

def set_gpt_model(userid, model):
    userdata = load_json(f"persistent/users/{userid}.json")
    
    if model == userdata[0]["model"]:
        return f"Model already in use. No changes made. Current model: {model}"
    else: 
        userdata[0]["model"] = model
        save_json(userdata, f"persistent/users/{userid}.json")
        return f"{model} Model set successfully!"


def clear_conversation(userid):
    userdata = load_json(f"persistent/users/{userid}.json")
    userdata = [userdata[0], userdata[1]]
    save_json(userdata, f"persistent/users/{userid}.json")
    return "Successfully cleared"


def custom_instructions(userid):
    userdata = load_json(f"persistent/users/{userid}.json")
    ai=f"Current custom instructions:\n'{userdata[1]['content']}'\n\nCustom instructions allow you to provide explicit guidance on how you want me to behave. Consider the questions below or provide me with any relevant information so that I can adjust my default behavior:\n\n-How formal or casual should I be?\n-How long or short should my responses generally be?\n-How do you want to be addressed?\n-Should I have opinions on topics or remain neutral?"
    append_message(userid, "user", "Let's Set The Custom Instructions!")
    append_message(userid, "assistant", ai)
    return ai


def set_custom_instructions(userid, instructions):
    userdata = load_json(f"persistent/users/{userid}.json")
    userdata = [userdata[0], userdata[1][instructions]]
    save_json(userdata, f"persistent/users/{userid}.json")
    return "Custom instructions Successfully Updated!"

    
def calculate_token_cost(response_data):
    # Access necessary data from the response_data
    model = response_data['model']
    usage = response_data['usage']
    
    if model == "gpt-3.5-turbo-0613":
        # Price for "gpt-3.5-turbo-0613"
        prompt_cost_per_k_tokens = 0.0015  
        completion_cost_per_k_tokens = 0.002 

    elif model == "gpt-4-0613":
        # Price for "gpt-4-0613"
        prompt_cost_per_k_tokens = 0.03
        completion_cost_per_k_tokens = 0.06
    else:
        print("Cannot calculate cost: Model not found")
        return
        
    prompt_tokens = usage["prompt_tokens"]
    completion_tokens = usage["completion_tokens"]
    # total_tokens = usage["total_tokens"]

    prompt_cost = (prompt_tokens / 1000) * prompt_cost_per_k_tokens
    completion_cost = (completion_tokens / 1000) * completion_cost_per_k_tokens

    total_cost = prompt_cost + completion_cost
    
    # format for readablility
    prompt_cost = "{:.8f}".format(prompt_cost)
    completion_cost = "{:.8f}".format(completion_cost)
    total_cost = "{:.8f}".format(total_cost)

    return total_cost


def update_balance(userid, cost):
    userdata = load_json(f"persistent/users/{userid}.json")
    cost = float(cost)
    credit = userdata[0]["usd_credit"]
    total_spent = userdata[0]["total_spent"]
    
    new_credit = credit - cost
    new_total_spent = total_spent + cost
    
    userdata[0]["usd_credit"] = new_credit
    userdata[0]["total_spent"] = new_total_spent
    
    save_json(userdata, f"persistent/users/{userid}.json")