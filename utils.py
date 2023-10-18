import json
import datetime
import os


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(name, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(name, indent=4, ensure_ascii=False))

def load_userdata(userid):
    user_path = os.path.abspath(f"persistent/users/{userid}.json")
    with open(user_path, "r") as f:
        return json.load(f)

def save_userdata(userid, userdata):
    user_path = os.path.abspath(f"persistent/users/{userid}.json")
    with open(user_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(userdata, indent=4, ensure_ascii=False))

def append_message(userid, role, content):
    userdata = load_userdata(userid)
    userdata.append({"role": role, "content": content})
    save_userdata(userid, userdata)
    return content

def context(userid, window=5):
    userdata = load_userdata(userid)
    return [userdata[1]] + userdata[2:][-int(window):]

def system_mess(userid):
    userdata = load_userdata(userid)
    return userdata[1]['content']

def userdata(userid, key):
    userdata = load_userdata(userid)
    return userdata[0][key]

def create_user(user):
    userdata = [
        {
            "userid": user.id,
            "joined": datetime.datetime.now().strftime("%Y-%m-%d")
,
            "username": user.username,
            "publicname": user.first_name,
            "btc_dep_addr": "N/A",   
            "model": "gpt-3.5-turbo",
            "temperature": 0.2,
            "max_tokens": 1024,
            "usd_credit": 1.00,
            "total_spent": 0.00 
        },
        {
            "role": "system",
            "content": f"You are a friendly Telegram bot powered by artificial intelligence. Your goal is to engage with & assist the user."
        }
    ]
    save_userdata(user.id, userdata)

def calculate_cost(response_data):
    # Access necessary data from the response_data
    model = response_data['model']
    usage = response_data['usage']['total_tokens']
    if model == "gpt-3.5-turbo-0613":
        cost = (usage / 1000) * 0.002 # Per 1k tokens
    elif model == "gpt-3.5-turbo-16k-0613":
        cost = (usage / 1000) * 0.004 # Per 1k tokens
    elif model == "gpt-4-0613":
        cost = (usage / 1000) * 0.06 # Per 1k tokens
    elif model == "gpt-4-32k-0613":
        cost = (usage / 1000) * 0.12 # Per 1k tokens
    else:
        print("Cannot calculate cost: Model not found")
        return
    # format for readablility
    return "{:.8f}".format(cost)

def update_balance(userid, cost):
    userdata = load_userdata(userid)
    cost = float(cost)
    credit = userdata[0]["usd_credit"]
    total_spent = userdata[0]["total_spent"]

    new_credit = credit - cost
    new_total_spent = total_spent + cost

    userdata[0]["usd_credit"] = new_credit
    userdata[0]["total_spent"] = new_total_spent

    save_userdata(userid, userdata)

def dashboard_messg(userid):
    userdata=load_userdata(userid)
    return """
    <b>Welcome to Your Account Dashboard!</b>

    <b>Joined:</b> """ + userdata[0]['joined'] + """
    <b>User ID:</b> """ + str(userdata[0]['userid']) + """
    <b>Username:</b> """ + userdata[0]['username'] + """
    <b>AI Model:</b> """ + userdata[0]['model'] + """

    <b>Balance:</b> $""" + f"{userdata[0]['usd_credit']:.4f}" + """
    <b>Total Spent:</b> $""" + f"{userdata[0]['total_spent']:.4f}" + """
    <b>Deposit BTC:</b> /add_credit

    <b>Settings</b>:
    /custom_instructions - The system propmt
    /clear_context - Delete conversation history

    <b>GPT-4 models</b>:
    /gpt4_0613 - $0.06/1k tokens
    /gpt4_32k_0613 - $0.12/1k tokens

    <b>GPT-3.5 models</b>:
    /gpt35_turbo_0613 - $0.002/1K tokens
    /gpt35_turbo_16k_0613 - $0.004/1K tokens

    <b>Feedback & Support</b>:
    <a href="https://t.me/dobe4ever">✉️ @dobe4ever</a>"""