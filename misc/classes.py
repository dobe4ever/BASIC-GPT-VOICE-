# from pydantic import BaseModel
# from typing import List, Dict

# # Define a Pydantic data class
# class UserData(BaseModel):
#     userid: int
#     username: str
#     publicname: str
#     btc_dep_addr: str  # Assuming this is a string, not an int
#     usd_credit: float  # Assuming this is a float, not a str
#     total_spent: float
#     model: str
    
#     system_message: Dict  # Assuming system_message is a dictionary
#     messages: List[Dict]  # Assuming messages is a list of dictionaries

# # Example data
# example_data = [{
#     "userid": 1,
#     "username": "JohnDoe",
#     "publicname": "John",
#     "btc_dep_addr": "1ABCDEF",
#     "usd_credit": 100.0,
#     "total_spent": 500.0,
#     "model": "gpt-3.5-turbo"
    
#     "system_message": {
#         "role": "system",
#         "content": "You are a friendly Telegram bot powered by artificial intelligence. Your goal is to engage with & assist the user."
#     },
#     "messages": [
#         {"role": "user", "content": "Hello, bot!"},
#         {"role": "bot", "content": "Hi there! How can I assist you today?"}
#     ]
# }

# # Create an instance of the data class with input data
# user_data = UserData(**example_data)

# # Print the validated data
# print(user_data.dict())

    
#     # userdata=[{
#     #     "userid": user_id,
#     #     "username": "",
#     #     "publicname": "",
#     #     "btc_dep_addr": "",   
#     #     "usd_credit": 1.0,
#     #     "total_spent": 0.0, 
#     #     "model": "gpt-3.5-turbo", 
#     # },
#     # {
#     #     "role": "system",
#     #     "content": f"You are a friendly Telegram bot powered by artificial intelligence. Your goal is to engage with & assist the user."
#     # }]


# # Create an instance of the data class with input data
# data = {"name": "Alice", "age": 30}
# person = Person(**data)

# # Print the validated data
# print(person.dict())







# # import json
# # import os
# # from dataclasses import dataclass

# # class UserData:
# #     DATA_PATH = "persistent/users"
# #     RECENT_MESSAGES_WINDOW = 5  # Adjust this as needed for the number of recent chat messages to store

# #     def __init__(self, user_id, username, first_name, btc_dep_addr, usd_credit, total_spent, model, role, content):
# #         self.user_id = user_id

# # Example usage:
# user_id = 548104065
# user = UserData(user_id)
# print(user.get_system_message())  # Access system message content
# print(user.get_recent_messages(2))  # Access the last 2 messages
# user.add_message(role="user", content="Hello!")
# user.add_message("assistant", "Hi there! How can I assist you today?")
# print(user.get_user_data("username"))  # Access username
# user.update_user_data("usd_credit", 10.0)  # Update USD credit




#         self.username = username
# #         self.first_name = first_name
# #         self.btc_dep_addr = btc_dep_addr
# #         self.usd_credit = usd_credit
# #         self.total_spent = total_spent
# #         self.model = model
# #         self.role = role
# #         self.content = content
        
# #         self.data = self.create_user()

# #     def create_user(self):
# #         user_data_path = os.path.join(self.DATA_PATH, f"{self.user_id}.json")
# #         if os.path.exists(user_data_path):
# #             with open(user_data_path, "r") as file:
# #                 return json.load(file)
# #         else:
# #             userdata=[{
# #                 "userid": user_id,
# #                 "username": "",
# #                 "publicname": "",
# #                 "btc_dep_addr": "",   
# #                 "usd_credit": 1.0,
# #                 "total_spent": 0.0, 
# #                 "model": "gpt-3.5-turbo", 
# #             },
# #             {
# #                 "role": "system",
# #                 "content": f"You are a friendly Telegram bot powered by artificial intelligence. Your goal is to engage with & assist the user."
# #             }]

    
# #     def save_user_data(self):
# #         user_data_path = os.path.join(self.DATA_PATH, f"{self.user_id}.json")
# #         with open(user_data_path, "w", encoding="utf-8") as f:
# #             f.write(json.dumps(name, indent=4, ensure_ascii=False))

# #     def set_system_message(self, user_id, content):
# #         self.data[1]["content"] = content
# #         self.save_user_data()

# #     def get_data(self, user_id, i, key):
# #         return self.data[i][key]
        
# #     def get_system_message(self, user_id):
# #         return self.data[1]["content"]

# #     def get_recent_messages(self, user_id, num_messages=5):
# #         return self.data[2:][-num_messages:]


# #     def add_message(self, user_id, role, content):
# #         messages = self.data[1:]
# #         messages.append({"role": role, "content": content})
# #         if len(messages) > self.RECENT_MESSAGES_WINDOW:
# #             messages.pop(0)  # Remove the oldest message if the window is full
# #         self.data["messages"] = messages
# #         self.save_user_data()


# # # Example usage:
# # user_id = 548104065
# # user = UserData(user_id)
# # print(user.get_system_message())  # Access system message content
# # print(user.get_recent_messages(2))  # Access the last 2 messages
# # user.add_message(role="user", content="Hello!")
# # user.add_message("assistant", "Hi there! How can I assist you today?")

# # print(user.get_data("username"))  # Access username
# # user.get_data("usd_credit", 10.0)  # Update USD credit



# import os
# import json


# def userdata(userid, key):
#     user_path = os.path.join("persistent/users/", f"{userid}.json")
#     if os.path.exists(user_path):
#         with open(user_path, "r") as f:
#             userdata=json.load(f)
#             return userdata[0][key]


# print(userdata(548104065, "btc_dep_addr"))