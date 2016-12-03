# -*- coding: utf-8 -*-
import os
import sys

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, FollowEvent, TextMessage, TextSendMessage,
)
import settings

app = Flask(__name__)


# get channel_secret and channel_access_token from your environment variable
channel_secret = settings.CHANNEL_SECRET
channel_access_token = settings.ACCESS_TOKEN
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)


#process line api keys
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/post", methods=['POST'])
def hook():
    #print(request.json)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'




@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    
    #docomo dialogue api
    msg = event.message.text

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg)
    )


# it starts when user follow this bot
@handler.add(FollowEvent)
def follow(event):


    # create message, which is sent when user add this bot as a friend
    msg = "Line追加ありがとう！\nお名前は何ですか?"

    # send an evaluation message
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg)
    )

    
if __name__ == "__main__":
    app.run()
