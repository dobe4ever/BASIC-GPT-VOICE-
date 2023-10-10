from keep_alive import keep_alive, keep_alive_ping
from utils import load_json, save_json, append_message, userdata, system_mess, user_key
from gpt_utils import run_conversation, transcribe_voice
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext # type: ignore
import threading
from typing import TYPE_CHECKING
from telegram import Bot, Update, ParseMode, ChatAction, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton # type: ignore
from persistent import CONSTANTS


# print(dir(telegram))
# help(telegram)

keep_alive_ping()

# Define the Telegram bot token & user id from the environment variable
bot_token = os.environ['BOT_TOKEN']
admin_id = int(os.environ['ADMIN_ID'])
bot = Bot(token=bot_token) 

def create_user(user):
    # Check if the user JSON file already exists
    if not os.path.exists(f"persistent/users/{user.id}.json"):
        # The file doesn't exist, so create the user

        btc_dep_addr = addresses["btc"][0]
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
                "temperature": 1,
                "max_tokens": 2048 
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
    bot.send_message(chat_id=user.id, text=response, reply_markup=CONSTANTS.reply_markup)
    
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
    user = userdata(userid)
    
    if user_message not in CONSTANTS.BUTTONS_TEXT:
        credit = user[0]['usd_credit']
        print(f"credit: {credit}")
        if credit > 0:
            # Pass the user message to GPT & get a response
            ai_response = run_conversation(userid, user_message) 
            # Respond to user on Telegram
            bot_send_text(userid, ai_response)
        else:
            bot_send_text(userid, "ERROR: Account out of credit")

    elif user_message in CONSTANTS.BUTTONS_TEXT:
        button(update)

def button(update):
    userid = update.message.from_user.id
    print(userid)

    if update.message.text == CONSTANTS.BUTTONS_TEXT[0]:  # account
        userdata=load_json(os.path.abspath(f"persistent/users/{userid}.json"))
        print(f"Button Text at index 0: {CONSTANTS.BUTTONS_TEXT[0]}")
        # Create a formatted message using Markdown
        message = (
            "Your Account Information:\n"
            f"*Username:* {userdata[0]['username']}\n"
            f"*BTC Deposit Address:* {userdata[0]['btc_dep_addr']}\n"
            f"*Account Balance:* ${userdata[0]['usd_credit']:.2f}\n"
            f"*Total Spent:* ${userdata[0]['total_spent']:.2f}\n"
            f"*AI Model:* {userdata[0]['model']}\n\n"
            "Transaction History:\n"
        )
        bot.send_message(chat_id=userid, text=message, reply_markup=CONSTANTS.reply_markup)

    elif update.message.text == CONSTANTS.BUTTONS_TEXT[1]:  # gpt3
        userdata=load_json(os.path.abspath(f"persistent/users/{userid}.json"))
        print(f"Button Text at index 1: {CONSTANTS.BUTTONS_TEXT[1]}")
        userdata[0]['model'] = "gpt-3.5-turbo"
        save_json(userdata, f"persistent/users/{userid}.json")
        bot_send_text(userid, "'gpt-3.5-turbo' model selected!")

    elif update.message.text == CONSTANTS.BUTTONS_TEXT[2]:  # gpt4
        userdata=load_json(os.path.abspath(f"persistent/users/{userid}.json"))
        print(f"Button Text at index 2: {CONSTANTS.BUTTONS_TEXT[2]}")
        userdata[0]['model'] = "gpt-4"
        save_json(userdata, f"persistent/users/{userid}.json")
        bot_send_text(userid, "'gpt-4' model selected!")

    elif update.message.text == CONSTANTS.BUTTONS_TEXT[3]:  # custom instruct
        userdata=load_json(os.path.abspath(f"persistent/users/{userid}.json"))
        print(f"Button Text at index 3: {CONSTANTS.BUTTONS_TEXT[3]}")
        reply_keyboard = [["Examples", "Help", "Cancel"]]
        text = f"Current instructions:\n\n'{userdata[1]['content']}'\n\nCustom instructions allow you to provide explicit guidance on how you want me to behave. Consider the questions below or provide me with any relevant information, and I will adjust my default behavior:\n\n-How formal or casual should I be?\n-How long or short should my responses generally be?\n-How do you want to be addressed?\n-Should I have opinions on topics or remain neutral?\n\nSend custom instructions"
        update.message.reply_text(
            text,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="I want you to act like a..."
            ),
        )
        append_message(userid, "user", "Lets set the custom instructions.")
        append_message(userid, "assistant", text)
        

    # elif update.message.text == CONSTANTS.BUTTONS_TEXT[3]:  # custom instruct
    #     userdata=load_json(os.path.abspath(f"persistent/users/{userid}.json"))
    #     print(f"Button Text at index 3: {CONSTANTS.BUTTONS_TEXT[3]}")
    #     reply_keyboard = [["Examples", "Help", "Cancel"]]
    #     print(f"Buttons inside index 3: {reply_keyboard}")
    #     text = f"Current instructions:\n\n'{system_mess(userid)}'\n\nCustom instructions allow you to provide explicit guidance on how you want me to behave. Consider the questions below or provide me with any relevant information and I will adjust my default behavior:\n\n-How formal or casual should I be?\n-How long or short should my responses generally be?\n-How do you want to be addressed?\n-Should I have opinions on topics or remain neutral?\n\nSend custom instructions"
    #     update.message.reply_text(
    #         text,
    #         reply_markup=ReplyKeyboardMarkup(
    #             reply_keyboard, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="I want you to act like a..."
    #         ),
    #     )
    #     append_message(userid, "user", "Lets set the custom instructions.")
    #     append_message(userid, "assistant", text)
        
        
    elif update.message.text == CONSTANTS.BUTTONS_TEXT[4]:  # clear conv
        userdata=load_json(os.path.abspath(f"persistent/users/{userid}.json"))
        print(f"Button Text at index 4: {CONSTANTS.BUTTONS_TEXT[4]}")
        userdata = [userdata[0], userdata[1]]
        save_json(userdata, f"persistent/users/{userid}.json")
        bot.send_message(chat_id=userid, text="Conversation cleared!", reply_markup=CONSTANTS.reply_markup)

    elif update.message.text == CONSTANTS.BUTTONS_TEXT[5]:  # Examples
        userdata=load_json(os.path.abspath(f"persistent/users/{userid}.json"))
        print(f"Button Text at index 5: {CONSTANTS.BUTTONS_TEXT[5]}")
        update.message.reply_text("Action Canceled", reply_markup=CONSTANTS.reply_markup)
        return

    elif update.message.text == CONSTANTS.BUTTONS_TEXT[6]:  # examples
        userdata=load_json(os.path.abspath(f"persistent/users/{userid}.json"))
        print(f"Button Text at index 6: {CONSTANTS.BUTTONS_TEXT[6]}")
        text = run_conversation(userid, "Please provide examples")
        update.message.reply_text(text, reply_markup=CONSTANTS.reply_markup)
        return

    elif update.message.text == CONSTANTS.BUTTONS_TEXT[7]:  # Help
        userdata=load_json(os.path.abspath(f"persistent/users/{userid}.json"))
        print(f"Button Text at index 7: {CONSTANTS.BUTTONS_TEXT[7]}")
        text = "HELP (button clicked by the user)"
        text = run_conversation(userid, "Please provide examples")
        update.message.reply_text("Action Canceled", reply_markup=CONSTANTS.reply_markup)

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