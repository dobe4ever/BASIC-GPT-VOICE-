# Standard Library Imports
import os
from typing import Union

# Third-party Package Imports
from telegram import Bot, Update, ParseMode, ChatAction # type: ignore
from telegram.ext import CallbackContext # type: ignore

# Project-specific Imports
from utils import userdata, load_json, save_json, append_message, system_mess, load_userdata, save_userdata, dashboard_messg, create_user
from gpt_utils import run_conversation, transcribe_voice
from speech import split_text, generate_audio, restart, elevenlabs_gen
from CONSTANTS import BUTTONS, WELCOME_MESSG, BOT_TOKEN, DEPOSIT_BTC_MESSG, CONTEXT_CLEARED_MSSG, NO_CREDIT_MESSG

# Define the Telegram bot token
bot = Bot(BOT_TOKEN) 

def check_credit(func):
    print(f"function running the check credit: {func}")
    def wrapper(update, context):
        userid = update.effective_user.id

        # If the user has no credit, send a message and stop processing other handlers
        if userdata(userid, 'usd_credit') <= 0:
            bot.send_message(
                chat_id=userid,
                text=NO_CREDIT_MESSG
            )
            print("No credit error message sent")  # Add this print statement
            return True  # Stop processing other handlers

        # If there is credit, run the function as intended
        return func(update, context)
    # Return the new function
    return wrapper
    
def is_new_user(update, context):
    # extract user info
    user = update.effective_user
    # if user doesn't exist, create a new user account
    user_path = os.path.abspath(f"persistent/users/{user.id}.json")
    if os.path.exists(user_path):
        print("is_new_user executed!")
        return None
    else:    
        create_user(user)
        bot.send_message(
            chat_id=user.id, 
            text=WELCOME_MESSG, 
            reply_markup=BUTTONS,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        return True

def clicked_button(update, context) -> Union[bool, None]:
    userid = update.message.from_user.id
    text = update.message.text
    print(f"Executing clicked_button:\text:\n{text}\n")
    
    if text == "My Account ⚙️":
        bot.send_message(
            chat_id=userid, 
            text=dashboard_messg(userid), 
            parse_mode="HTML", 
            disable_web_page_preview=True
        )
        return True

    elif text == "Clear Context ✨":
        clear_context(update, context)
        return True

    else: return

def start(update, context):
    userid = update.message.from_user.id
    userdata = load_userdata(userid)

    print("Executing start")

    bot.send_message(
        chat_id=userid, 
        text=dashboard_messg(userid), 
        reply_markup=BUTTONS,
        parse_mode="HTML", 
        disable_web_page_preview=True    
    )

def add_credit(update: Update, context: CallbackContext):
    userid = update.effective_user.id
    userdata = load_userdata(userid)

    print("Executing add credit command")

    bot.send_message(
        chat_id=userid, 
        text=DEPOSIT_BTC_MESSG, 
        parse_mode="Markdown", 
        disable_web_page_preview=True
    )

    bot.send_message(
        chat_id=userid, 
        text=f"`BTC ADDRESS: {userdata[0]['btc_dep_addr']}`",
        parse_mode="Markdown"
    )

@check_credit
def custom_instructions(update, context):
    userid = update.message.from_user.id
    userdata = load_userdata(userid)

    print("Executing /custom_instructions command")

    bot.send_message(
        chat_id=userid, 
        text="Custom instructions coming soon..."
    )
    return True

def clear_context(update, context):
    userid = update.effective_user.id
    userdata = load_userdata(userid)
    userdata = [userdata[0], userdata[1]]
    save_userdata(userid, userdata)
    bot.send_message(
        chat_id=userid, 
        text=CONTEXT_CLEARED_MSSG
    )
    return True

def gpt_4(update, context):
    userid = update.message.from_user.id
    userdata = load_userdata(userid)

    print("Executing gpt-4 command")

    userdata[0]['model'] = "gpt-4"
    save_userdata(userid, userdata)
    bot.send_message(
        chat_id=userid, 
        text="Using gpt-4 model (8k context)."
    )
    return True
    
def gpt4_32k(update, context):
    userid = update.message.from_user.id
    userdata = load_userdata(userid)

    print("Executing gpt4_32k command")

    userdata[0]['model'] = "gpt-4-32k"
    save_userdata(userid, userdata)
    bot.send_message(
        chat_id=userid, 
        text="Using gpt-4-32k (32k context)"
    )

def gpt35_turbo(update, context):
    userid = update.message.from_user.id
    userdata = load_userdata(userid)

    print("Executing gpt3_4k command")

    userdata[0]['model'] = "gpt-3.5-turbo"
    save_userdata(userid, userdata)
    bot.send_message(
        chat_id=userid, 
        text="Using gpt-3.5-turbo (4k context) model."
    )

def gpt35_turbo_16k(update, context):
    userid = update.message.from_user.id
    userdata = load_userdata(userid)

    print("Executing gpt3_16k command")

    userdata[0]['model'] = "gpt-3.5-turbo-16k"
    save_userdata(userid, userdata)
    bot.send_message(
        chat_id=userid, 
        text="Using gpt-3.5-turbo-16k (16k context)"
    )
        
@check_credit
def handle_voice(update, context):
    userid = update.message.from_user.id
    userdata = load_userdata(userid)
    # get voice
    file = bot.get_file(update.message.voice.file_id)
    # Get file extension from the file_path
    extension = file.file_path.split('.')[-1]
    # download voice
    file.download(f"downloads/voice-message.{extension}")
    # Open voice
    voice = open(os.path.abspath(
        f"downloads/voice-message.{extension}"), "rb")
    # transcribe voice
    transcript = transcribe_voice(voice)
    # Send transcript to GPT & get response
    ai_response = run_conversation(userid, transcript)
    # send Telegram message
    bot.sendChatAction(userid, action=ChatAction.TYPING)
    bot.send_message(userid, ai_response, parse_mode="Markdown")

@check_credit
def handle_text(update, context):
    userid = update.message.from_user.id
    text = update.message.text
    print(f"Executing handle_text:\ntext:\n{text}\n")

    if text == "My Account ⚙️" or text == "Clear Context ✨":
        return
    else:
        print(f"Executing handle_text:\ntext:\n{text}\n")
        # Pass the user message to GPT & get a response
        ai_response = run_conversation(userid, text) 

        # # send Telegram message
        # bot.sendChatAction(userid, action=ChatAction.TYPING)
        # bot.send_message(userid, ai_response, parse_mode="Markdown")
        # Respond to user on Telegram
        bot_send_audio(userid, ai_response)
        restart()


def bot_send_audio(userid, ai_response):
    # Generate audio response
    audio_message = elevenlabs_gen(ai_response)
    # Simulate recording voice message action on telegram
    bot.sendChatAction(chat_id=userid, action=ChatAction.RECORD_AUDIO)
    # Send audio message
    bot.send_document(chat_id=userid, document=audio_message)


