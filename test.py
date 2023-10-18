### python3 test.py

from elevenlabs import generate

from utils import load_userdata
from telegram import Bot, Update, ParseMode, ChatAction # type: ignore 
import os

# Define the bot token & user id from the env variable
bot_token = os.environ['BOT_TOKEN']
userid = int(os.environ['ADMIN_ID'])
bot = Bot(token=bot_token) 
#userdata=load_json(os.path.abspath(f"persistent/users/{userid}.json"))

def elevenlabs_gen(ai_response):
   # Optimize text message for speech
   paragraphs = split_text(text=ai_response)
   # Convert text to audio
   generate_audio(paragraphs)

   return open(os.path.abspath(f"downloads/audio-response.mp3"), "rb")


def split_text(text):
   # Split the text into chunks of 2400 characters each
   chunks = [text[i:i+2400] for i in range(0, len(text), 2400)]

   paragraphs = []

   for chunk in chunks:
       start = 0
       while start < len(chunk):
           # Find the closest period before the 230th character
           end = chunk.rfind('.', start, start + 230)

           if end == -1: 
               # If there is no period within the first 230 characters,
               # just cut off at the maximum length.
               end = min(start + 230, len(chunk))

           paragraph = chunk[start:end].strip()

           if paragraph: 
               paragraphs.append(paragraph)

           start = end + 1

   return paragraphs


def generate_audio(paragraphs):
   audio_files = []

   for paragraph in paragraphs:
       print(paragraph, "\n\n")

       # Generate audio for each paragraph
       audio = generate(
           text=paragraph,
           voice='Adam',
           # api_key="",
       )
       audio_files.append(audio)

   # Combine all audios into one and save it
   combined_audio = b"".join(audio_files)

   with open(os.path.abspath(
       f"downloads/audio-response.mp3"), "wb") as f:
           f.write(combined_audio)

def bot_send_audio(userid, ai_response):
    # Generate audio response
    audio_message = elevenlabs_gen(ai_response)
    # Simulate recording voice message action on telegram
    bot.sendChatAction(chat_id=userid, action=ChatAction.RECORD_AUDIO)
    # Send audio message
    bot.send_document(chat_id=userid, document=audio_message)


def restart():
   import subprocess
   SystemExit()
   subprocess.run(["kill", "1"])


### python3 test.py

ai_response="Thank you. I feel much better already having discussed these concerns with you. I'm looking forward to working together to improve my financial future."

elevenlabs_gen(ai_response)

bot_send_audio(userid, ai_response)

restart()

# Thank you for meeting with me, my name is Jonh Smith. I've been thinking about my financial future, and I'm not entirely sure if I'm on the right track. I hope you can help me address some concerns I have.

# Assistant: Of course, John. I'm here to help. Let's start by discussing your financial goals. What are you hoping to achieve in the short term and the long term?

# John Smith: Well, in the short term, I'd like to pay off my credit card debt and save for a family vacation. Long term, I want to make sure I have enough money for my children's education and a comfortable retirement.

# Assistant: Those are important goals, John. Let's delve into your current financial situation. Do you have a budget in place, and if so, is it working for you?

# John Smith: I do have a budget, but it often feels like I'm struggling to stick to it. I'm also concerned about my emergency fund. It's not as substantial as I'd like it to be.

# Assistant: I understand. We can definitely work on making your budget more manageable. It's essential that you're comfortable with it while also ensuring it helps you reach your goals. Now, regarding your emergency fund, how many months' worth of expenses do you have saved, and are you contributing to it regularly?

# John Smith: I have about two months' worth of expenses saved, and I do contribute to it, but I'm unsure if the amount is sufficient. Also, should I be investing some of it to make it grow?
##########################3
# Assistant: Good questions, John. Two months is a good start, but I usually recommend having at least three to six months' worth of living expenses in an emergency fund. We can discuss strategies to help you reach that goal. As for investing your emergency fund, it's generally best to keep it in a high-yield savings account or money market account for safety and liquidity.

# John Smith: That makes sense. I'm also thinking about my retirement savings. I have a 401(k), but I'm not sure if I'm contributing enough. How can I make sure I'm on track for a comfortable retirement?

# Assistant: Retirement planning is a vital aspect of your financial future. To determine if you're saving enough, we'll need to discuss your retirement goals, your current contributions, and your expected retirement age. We can then analyze if adjustments are needed to secure your retirement.

# John Smith: And what about my children's education fund? I want to make sure they have enough to attend the college of their choice.
########################################33
# Assistant: Saving for your children's education is commendable. We can explore options like 529 plans or other investment vehicles to help you grow these funds. It's essential to strike a balance between your retirement savings and your children's education goals.

# John Smith: Lastly, I've heard about sustainable investments, and I'm interested in aligning my investments with my values. How can I incorporate sustainable investing into my portfolio?

# Assistant: Sustainable and responsible investing is a growing trend. We can definitely incorporate this into your investment strategy by considering ESG (Environmental, Social, and Governance) factors when selecting investments. Let's explore how we can align your investments with your values while also meeting your financial objectives.

# John Smith: Thank you, Sarah. I feel much better already having discussed these concerns with you. I'm looking forward to working together to improve my financial future.

# Assistant: You're welcome, John. I'm here to help you every step of the way. Let's get started on a personalized financial plan that aligns with your goals and values.