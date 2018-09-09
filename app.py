# #Python libraries that we need to import for our bot
# import random
# from flask import Flask, request
# from pymessenger.bot import Bot
# import os
# # from pymessager.message import Messager

# app = Flask(__name__)

# ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
# VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

# bot = Bot(ACCESS_TOKEN)#PyMessenger

# # client = Messager(ACCESS_TOKEN)#PyMesssager
# #We will receive messages that Facebook sends our bot at this endpoint 
# @app.route("/", methods=['GET', 'POST'])

# def receive_message():
#     if request.method == 'GET':
#         """Before allowing people to message your bot, Facebook has implemented a verify token
#         that confirms all requests that your bot receives came from Facebook.""" 
#         token_sent = request.args.get("hub.verify_token")
#         return verify_fb_token(token_sent)
#     #if the request was not get, it must be POST and we can just proceed with sending a message back to user
#     else:
#         # get whatever message a user sent the bot
#        output = request.get_json()
#        for event in output['entry']:
#           messaging = event['messaging']
#           for message in messaging:
#             if message.get('message'):
#                 #Facebook Messenger ID for user so we know where to send response back to
#                 recipient_id = message['sender']['id']
#                 if message['message'].get('text'):
#                     response_sent_text = get_message()
#                     send_message(recipient_id, response_sent_text)
#                 #if user sends us a GIF, photo,video, or any other non-text item
#                 if message['message'].get('attachments'):
#                     response_sent_nontext = get_message()
#                     send_message(recipient_id, response_sent_nontext)
#     return "Message Processed"


# def verify_fb_token(token_sent):
#     #take token sent by facebook and verify it matches the verify token you sent
#     #if they match, allow the request, else return an error 
#     if token_sent == VERIFY_TOKEN:
#         return request.args.get("hub.challenge")
#     return 'Invalid verification token'


# #chooses a random message to send to the user
# def get_message():
#     sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "Good to know you :)"]
#     # return selected item to the user
#     return random.choice(sample_responses)

# #uses PyMessenger to send response to user
# def send_message(recipient_id, response):
#     #sends user the text message provided via input response parameter
#     bot.send_text_message(recipient_id, "Hello from PyMessenger")
#     # client.send_text(recipient_id, "Hello, I'm PyMessager.")
#     # bot.send_button_message(recepient_id,response,[
#     #           {
#     #             "type": "postback",
#     #             "title": "Yes",
#     #             "payload": "get_options"
#     #           },
#     #           {
#     #             "type": "postback",
#     #             "title": "No",
#     #             "payload": "no_options"
#     #           }
#     #         ])
#     # bot.send_text_message(recipient_id, "After button")
#     return "success"

# if __name__ == "__main__":
#     app.run()



import os
from flask import Flask, request
from fbmessenger import BaseMessenger
from fbmessenger import quick_replies
from fbmessenger.elements import Text
from fbmessenger.thread_settings import GreetingText, GetStartedButton, MessengerProfile

class Messenger(BaseMessenger):
    def __init__(self, page_access_token):
        self.page_access_token = page_access_token
        super(Messenger, self).__init__(self.page_access_token)

    def message(self, message):
        response = Text(text= str(message['message']['text']))
        action = response.to_dict()
        res = self.send(action)
        app.logger.debug('Response: {}'.format(res))

    def delivery(self, message):
        pass

    def read(self, message):
        pass

    def account_linking(self, message):
        pass

    def postback(self, message):
        payload = message['postback']['payload']

        if 'start' in payload:
            quick_reply_1 = quick_replies.QuickReply(title='Location', content_type='location')
            quick_replies_set = quick_replies.QuickReplies(quick_replies=[
                quick_reply_1
            ])
            text = {'text': 'Share your location'}
            text['quick_replies'] = quick_replies_set.to_dict()
            self.send(text)

    def optin(self, message):
        pass

    def init_bot(self):
        greeting_text = GreetingText('Welcome to weather bot')
        messenger_profile = MessengerProfile(greetings=[greeting_text])
        messenger.set_messenger_profile(messenger_profile.to_dict())

        get_started = GetStartedButton(payload='start')

        messenger_profile = MessengerProfile(get_started=get_started)
        messenger.set_messenger_profile(messenger_profile.to_dict())


app = Flask(__name__)
app.debug = True
messenger = Messenger(os.environ.get('ACCESS_TOKEN'))


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == os.environ.get('VERIFY_TOKEN'):
            messenger.init_bot()
            return request.args.get('hub.challenge')
        raise ValueError('FB_VERIFY_TOKEN does not match.')
    elif request.method == 'POST':
        messenger.handle(request.get_json(force=True))
    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0')
