import os
import threading
import telegram
from telegram import Bot, Update, ParseMode, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Filters, MessageHandler, Updater, CallbackContext, CommandHandler
from utils import handle_setting
from gpt_utils import transcribe_voice, run_conversation
from keep_alive import keep_alive, keep_alive_ping

keep_alive_ping()

# Define the Telegram bot token & user id from the environment variable
bot_token = os.environ['BOT_TOKEN']
admin_id = int(os.environ['ADMIN_ID'])
bot = Bot(token=bot_token)  


def bot_send_text(text):
    # Simulate typing action on telegram
    bot.sendChatAction(chat_id=admin_id, action=telegram.ChatAction.TYPING)
    # Send text message
    bot.send_message(text=text, chat_id=admin_id, parse_mode=ParseMode.MARKDOWN)


def handle_settings(message):
    # Check if settings message
    if message == "Use GPT-3.5" or message == "Use GPT-4" or message == "Clear Conversation" or message == "Custom Instructions": 
        result = handle_setting(message)
        bot_send_text(result)
        return True
    else:
        return False


def handle_text(update: Update, context):
    # Check if the message was sent from the specified user ID
    if update.message.from_user.id == admin_id:       
        if handle_settings(update.message.text):
            return
        else:    
            # Pass the user message to GPT & get a response
            ai_response = run_conversation(update.message.text) 
            # Respond to user on Telegram
            bot_send_text(ai_response)
    
    
def handle_voice(update: Update, context):
    # Check if the message was sent from the specified user ID
    if update.message.from_user.id == admin_id:  
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
        ai_response = run_conversation(transcript)
        # Respond to user on Telegram
        bot_send_text(ai_response)


def start(update: Update, context: CallbackContext):
    # Check if the message was sent from the specified user ID
    if update.message.from_user.id == admin_id: 
        # create menu
        settings_menu = [
            [
                KeyboardButton("Use GPT-3.5"),
                KeyboardButton("Use GPT-4")
            ],
            [
                KeyboardButton("Clear Conversation")
            ],
            [
                KeyboardButton("Custom Instructions")
            ]            
        ]
        ai_response = run_conversation("Hello!")
        bot.send_message(
            chat_id=admin_id, 
            text=ai_response,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=settings_menu, resize_keyboard=True))
        


def main():
    # Create an instance of the Updater class using the bot token
    updater = Updater(token=bot_token, use_context=True)
    dp = updater.dispatcher

    # add the start command
    dp.add_handler(CommandHandler("start", start))

    # Create handler to capture audio messages
    dp.add_handler(MessageHandler(Filters.voice & ~Filters.text, handle_voice))
    
    # Register the handler for all incoming text messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
        
    # Start the bot
    updater.start_polling()
    
    keep_alive_thread = threading.Thread(target=keep_alive)
    keep_alive_thread.daemon = True
    keep_alive_thread.start()

    updater.idle()
    updater.stop()

if __name__ == '__main__':
    main()
