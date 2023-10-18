from keep_alive import keep_alive, keep_alive_ping

import threading
from typing import TYPE_CHECKING

from telegram import Bot, Update, ParseMode, ChatAction # type: ignore
from telegram.ext import (
Updater, CommandHandler, MessageHandler, Filters # type: ignore
)
from tg_utils import (
is_new_user, add_credit_cmd, clear_context_cmd, 
gpt35_turbo_0613_cmd, gpt35_turbo_16k_0613_cmd, gpt4_0613_cmd,
gpt4_32k_0613_cmd, start_cmd, 
custom_instructions_cmd, clicked_button, handle_voice, 
handle_text
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

    # # Handle if the user has no credit
    # dp.add_handler(MessageHandler(
    #     Filters.all, has_no_credit), group=0)

    # Handle if the user clicked a button
    dp.add_handler(MessageHandler(
        Filters.text & ~Filters.command, clicked_button), group=1)

    # handle setting commands
    dp.add_handler(CommandHandler(
        "start", start_cmd), group=1)
    dp.add_handler(CommandHandler(
        "add_credit", add_credit_cmd), group=1)
    dp.add_handler(CommandHandler(
        "custom_instructions", custom_instructions_cmd), group=2)
    dp.add_handler(CommandHandler(
        "clear_context", clear_context_cmd), group=1)
    # handle model commands
    dp.add_handler(CommandHandler(
        "gpt35_turbo_0613", gpt35_turbo_0613_cmd), group=1)
    dp.add_handler(CommandHandler(
        "gpt35_turbo_16k_0613",gpt35_turbo_16k_0613_cmd), group=1)
    dp.add_handler(CommandHandler(
        "gpt4_0613", gpt4_0613_cmd), group=1)
    dp.add_handler(CommandHandler(
        "gpt4_32k_0613", gpt4_32k_0613_cmd), group=1)

    
    # handle voice messages
    dp.add_handler(MessageHandler(
        Filters.voice & ~Filters.text, handle_voice), group=3)
    
    # handle all other text messages
    dp.add_handler(MessageHandler(
        Filters.text & Filters.entity & ~Filters.command, handle_text), group=3)


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
