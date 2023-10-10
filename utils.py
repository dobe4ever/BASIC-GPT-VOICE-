from datetime import datetime
import json
import pytz
from elevenlabs import generate
import openai
import os

# Define the OpenAI key from the environment variable
openai.api_key = os.environ['OPENAI_API_KEY']

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)
        
def save_json(name, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(name, indent=4, ensure_ascii=False))

def userdata(userid):
    user_path = os.path.abspath(f"persistent/users/{userid}.json")
    with open(user_path, "r") as f:
        return json.load(f)
            
def system_mess(userid):
    user_path = os.path.abspath(f"persistent/users/{userid}.json")
    if os.path.exists(user_path):
        with open(user_path, "r") as f:
            userdata=json.load(f)
            return userdata[1]['content']
            
def user_key(userid, key):
    user_path = os.path.abspath(f"persistent/users/{userid}.json")
    if os.path.exists(user_path):
        with open(user_path, "r") as f:
            userdata=json.load(f)
            return userdata[0][key]
# print(userdata(548104065, "btc_dep_addr"))


def append_message(userid, role, content):
    # Load user data
    userdata = load_json(f"persistent/users/{userid}.json")
    # Append message to the conversation history
    userdata.append({"role": role, "content": content})
    # Save conversation history
    save_json(userdata, f"persistent/users/{userid}.json")
    return userdata

def calculate_token_cost(response_data):
    # Access necessary data from the response_data
    model = response_data['model']
    usage = response_data['usage']
    if model == "gpt-3.5-turbo-0613":
        # Price for "gpt-3.5-turbo-0613"
        prompt_cost_per_k_tokens = 0.005
    elif model == "gpt-4-0613":
        # Price for "gpt-4-0613"
        prompt_cost_per_k_tokens = 0.08
    else:
        print("Cannot calculate cost: Model not found")
        return
    total_tokens = usage["total_tokens"]
    cost = (total_tokens / 1000) * prompt_cost_per_k_tokens
    # format for readablility
    return "{:.8f}".format(cost)


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