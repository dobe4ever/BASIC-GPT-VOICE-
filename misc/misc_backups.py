
# def button(update):
#     userid = update.message.from_user.id
#     print(userid)

#     if update.message.text == CONSTANTS.BUTTONS_TEXT[0]:  # account
#         userdata=load_json(os.path.abspath(f"persistent/users/{userid}.json"))
#         print(f"Button Text at index 0: {CONSTANTS.BUTTONS_TEXT[0]}")
#         # Create a formatted message using Markdown
#         message = (
#             "Your Account Information:\n"
#             f"*Username:* {userdata[0]['username']}\n"
#             f"*BTC Deposit Address:* {userdata[0]['btc_dep_addr']}\n"
#             f"*Account Balance:* ${userdata[0]['usd_credit']:.2f}\n"
#             f"*Total Spent:* ${userdata[0]['total_spent']:.2f}\n"
#             f"*AI Model:* {userdata[0]['model']}\n\n"
#             "Transaction History:\n"
#         )
#         bot.send_message(chat_id=userid, text=message, reply_markup=CONSTANTS.reply_markup)

#     elif update.message.text == CONSTANTS.BUTTONS_TEXT[1]:  # gpt3
#         userdata=load_json(os.path.abspath(f"persistent/users/{userid}.json"))
#         print(f"Button Text at index 1: {CONSTANTS.BUTTONS_TEXT[1]}")
#         userdata[0]['model'] = "gpt-3.5-turbo"
#         save_json(userdata, f"persistent/users/{userid}.json")
#         bot_send_text(userid, "'gpt-3.5-turbo' model selected!")

#     elif update.message.text == CONSTANTS.BUTTONS_TEXT[2]:  # gpt4
#         userdata=load_json(os.path.abspath(f"persistent/users/{userid}.json"))
#         print(f"Button Text at index 2: {CONSTANTS.BUTTONS_TEXT[2]}")
#         userdata[0]['model'] = "gpt-4"
#         save_json(userdata, f"persistent/users/{userid}.json")
#         bot_send_text(userid, "'gpt-4' model selected!")

#     elif update.message.text == CONSTANTS.BUTTONS_TEXT[3]:  # custom instruct
#         userdata=load_json(os.path.abspath(f"persistent/users/{userid}.json"))
#         print(f"Button Text at index 3: {CONSTANTS.BUTTONS_TEXT[3]}")
#         reply_keyboard = [["Examples", "Help", "Cancel"]]
#         text = f"Current instructions:\n\n'{userdata[1]['content']}'\n\nCustom instructions allow you to provide explicit guidance on how you want me to behave. Consider the questions below or provide me with any relevant information, and I will adjust my default behavior:\n\n-How formal or casual should I be?\n-How long or short should my responses generally be?\n-How do you want to be addressed?\n-Should I have opinions on topics or remain neutral?\n\nSend custom instructions"
#         update.message.reply_text(
#             text,
#             reply_markup=ReplyKeyboardMarkup(
#                 reply_keyboard, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="I want you to act like a..."
#             ),
#         )
#         append_message(userid, "user", "Lets set the custom instructions.")
#         append_message(userid, "assistant", text)
        

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
        
        
    # elif update.message.text == CONSTANTS.BUTTONS_TEXT[4]:  # clear conv
    #     userdata=load_json(os.path.abspath(f"persistent/users/{userid}.json"))
    #     print(f"Button Text at index 4: {CONSTANTS.BUTTONS_TEXT[4]}")
    #     userdata = [userdata[0], userdata[1]]
    #     save_json(userdata, f"persistent/users/{userid}.json")
    #     bot.send_message(chat_id=userid, text="Conversation cleared!", reply_markup=CONSTANTS.reply_markup)

    # elif update.message.text == CONSTANTS.BUTTONS_TEXT[5]:  # Examples
    #     userdata=load_json(os.path.abspath(f"persistent/users/{userid}.json"))
    #     print(f"Button Text at index 5: {CONSTANTS.BUTTONS_TEXT[5]}")
    #     update.message.reply_text("Action Canceled", reply_markup=CONSTANTS.reply_markup)
    #     return

    # elif update.message.text == CONSTANTS.BUTTONS_TEXT[6]:  # examples
    #     userdata=load_json(os.path.abspath(f"persistent/users/{userid}.json"))
    #     print(f"Button Text at index 6: {CONSTANTS.BUTTONS_TEXT[6]}")
    #     text = run_conversation(userid, "Please provide examples")
    #     update.message.reply_text(text, reply_markup=CONSTANTS.reply_markup)
    #     return

    # elif update.message.text == CONSTANTS.BUTTONS_TEXT[7]:  # Help
    #     userdata=load_json(os.path.abspath(f"persistent/users/{userid}.json"))
    #     print(f"Button Text at index 7: {CONSTANTS.BUTTONS_TEXT[7]}")
    #     text = "HELP (button clicked by the user)"
    #     text = run_conversation(userid, "Please provide examples")
    #     update.message.reply_text("Action Canceled", reply_markup=CONSTANTS.reply_markup)

    #     return