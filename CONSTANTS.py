from telegram import KeyboardButton, ReplyKeyboardMarkup # type: ignore
import os

BOT_TOKEN = os.environ['BOT_TOKEN']

WELCOME_MESSG = """
Welcome! You got some free credits! 

✨ Use the magic of GPT-3.5 & GPT-4 through our API.
🚀 Get started now & let your imagination run wild.

Happy chatting!
"""

NO_CREDIT_MESSG = "ERROR: No credit. /add_credit"

DEPOSIT_BTC_MESSG = """
Pay-as-you-go: Pricing ranges from $0.002 to $0.06 per 1k tokens (about 700 words). We're practically giving it away, making it accessible to all without needing a PLUS OpenAI subscription.

Coin: *BTC*
Network: *Bitcoin – BTC* ‼️

⚡️ Send any amount to the address below, and it'll be converted and added to your USD balance.

⚠️ Send only *BTC* via *Bitcoin* to this address, otherwise coins will be lost.

✅ No fees: Exchange rate based on Yahoo Finance when BTC confirms.
"""

CONTEXT_CLEARED_MSSG = "Conversation history has been cleared."

BUTTONS = ReplyKeyboardMarkup(
    [
        [KeyboardButton("My Account ⚙️")],
        [KeyboardButton("Clear Context ✨")]
    ], 
    resize_keyboard=True
)
