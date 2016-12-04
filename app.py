# -*- coding: utf-8 -*-
import os
import sys
import datetime
import time
import requests

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, URITemplateAction, PostbackTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

import settings
from connectDB import *
from defTimes import *
from sendmsg import * 

from doco.client import Client
from pymongo import MongoClient
app = Flask(__name__)


#docomo conversation api key
docomo_api_key = settings.DOCOMO_API_KEY
if docomo_api_key is None:
    print("DOCOMO_API_KEY not found")
    sys.exit(1)

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

#process docomo api key
user = settings.user_config
doco = Client(docomo_api_key, user=user)


#post request to line bot server from ifttt, which is connected to mesh 
@app.route("/post", methods=['POST'])
def hook():

    #weather information
 
    r = requests.get(settings.HEART_BEAT + "weather")
    contents = r.content.decode('utf-8')

    buttons_template_message = TemplateSendMessage(
        alt_text='この情報はスマートフォンからのみ観覧できます。',
        template=ButtonsTemplate(
            text= "天気予報" + contents,
            actions=[
                URITemplateAction(
                    label='詳しく!',
                    uri='http://weather.yahoo.co.jp/weather/jp/13/4410.html'
                )
            ]
        )
    )
    
    line_bot_api.push_message("U41a55a88dcc95a269aacdf0e9c112361", buttons_template_message)

    time.sleep(1.0)

    #get times
    times, today_1 = getNowTimes()
    
    #connect to database
    dbh, stmt = connectDB()
    sql = "select * from take where appointed_time like " + '"' + today_1 + "%" + '"' + ';'
    stmt.execute(sql)
    rows = stmt.fetchall()
    for row in rows:
        message = SendMsg(row)         
        line_bot_api.push_message("U41a55a88dcc95a269aacdf0e9c112361", TextSendMessage(text=message))



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
    response = doco.send(utt=msg, apiname="Dialogue")

    if "今日の予定" in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="今日はまだ予定ないよ")
        )

    if "予定を入力する" == event.message.text:


         
        buttons_template_message = TemplateSendMessage(
            alt_text='この情報はスマートフォンからのみ観覧できます。',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/bot/images/item2.jpg',
                title='予定を追加？',
                text='新しい予定を入力しますか？',
                actions=[
                    URITemplateAction(
                        label='入力する',
                        uri="https://lastiothack.herokuapp.com/inputpage/"
                    )
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            buttons_template_message
        )

    #mid = event.source.userId
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response['utt'])
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
