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


def append_message(role, content):
    # Load conversation history
    conversation = load_json("conversation.json")
    # Append message to the conversation history
    conversation.append({"role": role, "content": content})
    # Save conversation history
    save_json(conversation, "conversation.json")

    return conversation


def set_gpt_model(model):
    settings = load_json("settings.json")
    
    if model == "Use GPT-3.5":
        model = "gpt-3.5-turbo"
        if settings["model"] == model:   
            return "Model already in use. No Changes made."
        else: 
            settings["model"] = model
            save_json(settings, "settings.json")
            return "GPT-3.5 Turbo Model Set Successfully!"
            
    elif model == "Use GPT-4":        
        model = "gpt-4"
        if settings["model"] == model:   
            return "Model already in use. No Changes made."
        else: 
            settings["model"] = model
            save_json(settings, "settings.json")
            return "GPT-4 Model Set Successfully!"

    else:
        return "ERROR: Invalid model"


def clear_conversation():
    conversation = load_json("conversation.json")
    conversation = [conversation[0]]
    save_json(conversation, "conversation.json")
    return "Successfully cleared"


def custom_instructions():
    conversation = load_json("conversation.json")
    
    ai=f"Current custom instructions:\n'{conversation[0]['content']}'\n\nCustom instructions allow you to provide explicit guidance on how you want me to behave. Consider the questions below or provide me with any relevant information so that I can adjust my default behavior:\n\n-How formal or casual should I be?\n-How long or short should my responses generally be?\n-How do you want to be addressed?\n-Should I have opinions on topics or remain neutral?"
    
    append_message("user", "Let's Set The Custom Instructions!")
    append_message("assistant", ai)

    return ai
    
def handle_setting(setting):
    if setting == "Use GPT-3.5" or setting == "Use GPT-4":
        return set_gpt_model(setting)
    if setting == "Clear Conversation":
        return clear_conversation()
    if setting == "Custom Instructions":
        return custom_instructions()
    else: pass