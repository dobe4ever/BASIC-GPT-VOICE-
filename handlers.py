from utils import load_userdata, save_userdata, append_message
from telegram import ReplyKeyboardMarkup # type: ignore
import json
import os

# Command handler for /add_credit
def add_credit(update, context):
    userid = update.effective_user.id
    userdata = load_userdata(userid)

    # Modify user data to add credit
    userdata[0]["usd_credit"] += 1.0  # You can adjust the credit as needed

    # Save the updated user data
    save_userdata(userid, userdata)

    # Send a response back to the user
    update.message.reply_text(f"Added $1.00 to your account. Your new balance is ${userdata[0]['usd_credit']}.")

