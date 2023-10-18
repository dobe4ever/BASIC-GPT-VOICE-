from keep_alive import keep_alive, keep_alive_ping

import threading
from typing import TYPE_CHECKING

from telegram import Bot, Update, ParseMode, ChatAction # type: ignore
from telegram.ext import (
Updater, CommandHandler, MessageHandler, Filters # type: ignore
)
from tg_utils import (
start, is_new_user, add_credit, clear_context, 
gpt35_turbo_16k, gpt35_turbo, gpt4_32k, gpt_4,
custom_instructions, clicked_button, 
handle_voice, handle_text
)
from CONSTANTS import BOT_TOKEN

keep_alive_ping()

def main():
    # Instanciate the Updater class with the bot token
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Handle a new user
    dp.add_handler(MessageHandler(
        Filters.all, is_new_user), group=0)
    
    # Handle if the user clicked a button
    dp.add_handler(MessageHandler(
        Filters.text & ~Filters.command, clicked_button), group=1)

    # # Handle if the user has no credit
    # dp.add_handler(MessageHandler(
    #     Filters.all, has_no_credit), group=0)

    # handle setting commands
    dp.add_handler(CommandHandler(
        "start", start), group=1)
    dp.add_handler(CommandHandler(
        "add_credit", add_credit), group=1)
    dp.add_handler(CommandHandler(
        "clear_context", clear_context), group=1)
    # handle model commands
    dp.add_handler(CommandHandler(
        "gpt_4", gpt_4), group=1)
    dp.add_handler(CommandHandler(
        "gpt_4_32k", gpt4_32k), group=1)
    dp.add_handler(CommandHandler(
        "gpt35_turbo", gpt35_turbo), group=1)
    dp.add_handler(CommandHandler(
        "gpt35_turbo_16k",gpt35_turbo_16k), group=1)
    
    # handle voice messages
    dp.add_handler(MessageHandler(
        Filters.voice & ~Filters.text, handle_voice), group=2)
    
    # handle all other text messages
    dp.add_handler(MessageHandler(
        Filters.text & Filters.entity & ~Filters.command, handle_text), group=2)

    # handle custom instructions last
    dp.add_handler(CommandHandler(
        "custom_instructions", custom_instructions), group=1)

    # Start the bot
    updater.start_polling()

    keep_alive_thread = threading.Thread(target=keep_alive)
    keep_alive_thread.daemon = True
    keep_alive_thread.start()

    updater.idle()
    updater.stop()

if __name__ == '__main__':
    main()

# # Command handler for /custom_instructions
# def custom_instructions(update, context):
#     userid = update.message.from_user.id
#     text = f"Current instructions:\n\n'{system_mess(userid)}'\n\nCustom instructions allow you to provide explicit guidance on how you want me to behave. Consider the questions below or provide me with any relevant information, and I will adjust my default behavior:\n\n-How formal or casual should I be?\n-How long or short should my responses generally be?\n-How do you want to be addressed?\n-Should I have opinions on topics or remain neutral?\n\nSend custom instructions"
#     bot.sendChatAction(userid, action=ChatAction.TYPING)
#     update.message.reply_text(
#         text, reply_markup=ReplyKeyboardRemove(),
#     )
#     append_message(userid, "user", "Lets set the custom instructions.")
#     append_message(userid, "assistant", text)
