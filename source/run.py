from nlu_process import main
from wxpy import *

bot = Bot()
my_friend = bot.friends().search('Chat_Bot')[0]
res = main.Respond()


@bot.register(my_friend)
def forward_message(msg):
    if msg.type == 'Text':
        print("USER: {}".format(msg.text))
        response = res.send_message(msg.text)
        print("BOT: {}".format(response))
        return response
    else:
        return "please use text to chat with me"

bot.join()


# res = main.Respond()
# def send_messages(messages):
#     for msg in messages:
#         print("USER: {}".format(msg))
#         response = res.send_message(msg)
#         print(response)
#
# send_messages([
#     "tell me the ranks",
#     "Premier league",
#     "what's the match of PL?",
#     "do you think liverpool can win",
#     "Bye bye"
# ])