from keep_alive import keep_alive, keep_alive_ping
from utils import load_json, save_json, append_message
from gpt_utils import run_conversation, transcribe_voice
import os

# userdata = load_json("persistent/users/548104065.json")
# print(f"userdata: {userdata}\n\n")
# print(f"model: {userdata[0]['model']}\n\n")
# print(f"system object: {userdata[1]}\n\n")
# print(f"system content: {userdata[1]['content']}\n\n")


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext # type: ignore
import threading
from typing import TYPE_CHECKING
from telegram import Bot, Update, ParseMode, ChatAction, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton # menubutton  # type: ignore
# print(dir(telegram))
# help(telegram)

keep_alive_ping()

# Define the Telegram bot token & user id from the environment variable
bot_token = os.environ['BOT_TOKEN']
admin_id = int(os.environ['ADMIN_ID'])
bot = Bot(token=bot_token) 


# Create settings menu
BUTTONS = [
    [KeyboardButton("My Account")],           
    [KeyboardButton("Use GPT-3.5"), KeyboardButton("Use GPT-4")],           
    [KeyboardButton("Custom Instructions")],
    [KeyboardButton("Clear Conversation")]
]
BUTTONS_TEXT = [
    "My Account",           
    "Use GPT-3.5",
    "Use GPT-4",
    "Custom Instructions",
    "CANCEL",
    "Examples",
    "Help"
]
reply_markup=ReplyKeyboardMarkup(
    BUTTONS, resize_keyboard=True
)


def create_user(user):
    # Check if the user JSON file already exists
    if not os.path.exists(f"persistent/users/{user.id}.json"):
        # The file doesn't exist, so create the user
        addresses = load_json(
            "persistent/crypto_addresses/crypto_addresses.json")
        print(addresses)
        btc_dep_addr = addresses["btc"][0]
        del addresses["btc"][0]
        save_json(addresses, "persistent/crypto_addresses/crypto_addresses.json")
        
        # create user data file
        path=f"persistent/users/{user.id}.json"
        userdata=[
            {
                "userid": user.id,
                "username": user.username,
                "publicname": user.first_name,
                "btc_dep_addr": btc_dep_addr,   
                "usd_credit": 1.0,
                "total_spent": 0.0, 
                "model": "gpt-3.5-turbo", 
            },
            {
                "role": "system",
                "content": f"You are a friendly Telegram bot powered by artificial intelligence. Your goal is to engage with & assist the user."
            },
        ]
        save_json(userdata, path) 
    # if user already exists    
    else: pass 

def bot_send_text(userid, text):
    # Simulate typing action on telegram
    bot.sendChatAction(chat_id=userid, action=ChatAction.TYPING)
    # Send text message
    bot.send_message(text=text, chat_id=userid, parse_mode=ParseMode.MARKDOWN)

def start(update: Update, context: CallbackContext):
    # Extract user info
    user = update.message.from_user
    # create userdata if not exist
    create_user(user)
    # send 'Hello!' to GPT to generate response
    response = run_conversation(user.id, "Hello!")
    # send Telegram message
    bot.send_message(chat_id=user.id, text=response, reply_markup=reply_markup)
    
def handle_voice(update: Update, context):
    userid = update.message.from_user.id
    userdata = load_json(f"{userid}.json")
    if userdata[0]["usd_credit"] > 0:
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
        # Respond to user on Telegram
        bot_send_text(userid, ai_response)

def handle_text(update: Update, context):
    userid = update.message.from_user.id
    user_message = update.message.text
    
    userdata = load_json(f"persistent/users/{userid}.json")
    
    if user_message not in BUTTONS_TEXT:
        if userdata[0]["usd_credit"] > 0:
            # Pass the user message to GPT & get a response
            ai_response = run_conversation(userid, user_message) 
            # Respond to user on Telegram
            bot_send_text(userid, ai_response)
        else:
            bot_send_text(userid, "ERROR: Account out of credit")

    elif user_message in BUTTONS_TEXT:
        button(update)

def button(update):
    userid=update.message.from_user.id
    userdata = load_json(f"persistent/users/{userid}.json")
    
    if update.message.text == BUTTONS_TEXT[0]: # account
        pass
        
    elif update.message.text == BUTTONS_TEXT[1]: # gpt3
        userdata[0]['model'] = "gpt-3.5-turbo"
        save_json(userdata, f"persistent/users/{userid}.json")
        bot_send_text(userid, "'gpt-3.5-turbo' model selected!")
        
    elif update.message.text == BUTTONS_TEXT[2]: # gpt4
        userdata[0]['model'] = "gpt-4"
        save_json(userdata, f"persistent/users/{userid}.json")
        bot_send_text(userid, "'gpt-4' model selected!")

    elif update.message.text == BUTTONS_TEXT[3]: # custom instruct
        reply_keyboard = [["Examples", "Help", "Cancel"]]
        text=f"Current instructions:\n\n'{userdata[1]['content']}'\n\nCustom instructions allow you to provide explicit guidance on how you want me to behave. Consider the questions below or provide me with any relevant information and I will adjust my default behavior:\n\n-How formal or casual should I be?\n-How long or short should my responses generally be?\n-How do you want to be addressed?\n-Should I have opinions on topics or remain neutral?\n\nSend custom instructions"
        update.message.reply_text(
            text,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="I want you to act like a..."
            ),
        )
        append_message(userid, "user", "Lets set the custom instructions.")
        append_message(userid, "assistant", text)

    elif update.message.text == BUTTONS_TEXT[4]: # clear conv
        userdata = [userdata[0], userdata[1]]
        save_json(userdata, f"persistent/users/{userid}.json")
        bot.send_message(chat_id=userid, text="Conversation cleared!", reply_markup=reply_markup)

    elif update.message.text == BUTTONS_TEXT[5]: # CANCEL
        update.message.reply_text("Action Canceled", reply_markup=reply_markup)
        return 

    elif update.message.text == BUTTONS_TEXT[6]: # Examples
        text=run_conversation(userid, "Please provide examples")
        update.message.reply_text(text, reply_markup=reply_markup)
        return 

    elif update.message.text == BUTTONS_TEXT[7]: # Help
        text="The user just clicked the 'Help' button. Consider whether or not there's enough information in the current conversation to provide help. When unsure, ask for aditional information to make sure you get it right."
        text=run_conversation(userid, "Please provide examples")
        update.message.reply_text("Action Canceled", reply_markup=reply_markup)
        return 


def main():
    # Create an instance of the Updater class using the bot token
    updater = Updater(token=bot_token, use_context=True)
    dp = updater.dispatcher
    
    # Create handler for the /start command
    dp.add_handler(CommandHandler('start', start))
    
    # Create handler to capture audio messages
    dp.add_handler(MessageHandler(Filters.voice & ~Filters.text, handle_voice))
    
    # Register the handler for all incoming text messages
    dp.add_handler(MessageHandler(Filters.text & Filters.entity & ~Filters.command, handle_text))
        
    # Start the bot
    updater.start_polling()
    
    keep_alive_thread = threading.Thread(target=keep_alive)
    keep_alive_thread.daemon = True
    keep_alive_thread.start()

    updater.idle()
    updater.stop()


if __name__ == '__main__':
    main()