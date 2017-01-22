# -*- coding: utf-8 -*-
import os
import sys
import datetime
import time
import requests
import psycopg2

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
 
    #r = requests.get(settings.HEART_BEAT + "weather")
    #contents = r.content.decode('utf-8')

   # buttons_template_message = TemplateSendMessage(
   #     alt_text='この情報はスマートフォンからのみ観覧できます。',
   #     template=ButtonsTemplate(
   #         title='天気予報',
   #         text= contents[285:319],
   #         actions=[
   #             URITemplateAction(
   #                 label='詳しく!',
   #                 uri='http://weather.yahoo.co.jp/weather/jp/13/4410.html'
   #             )
   #         ]
   #     )
   # )
    
   # line_bot_api.push_message("U41a55a88dcc95a269aacdf0e9c112361", buttons_template_message)

    #get now time
    todayHM, todayYMD = getNowTimes()
    
    #connect to database
    db = usePSQL(settings.host, settings.db, settings.user, settings.password)
    
    #fetch datas
    result = db.getAllAppointments(todayHM, todayYMD)
    message = sendAllMsg(result, todayHM)    
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
    

    msg = event.message.text
    
    #docomo dialogue api
    response = doco.send(utt=msg, apiname="Dialogue")

    if "今日の予定" in msg:
        todayHM, todayYMD = getNowTimes()
        db = usePSQL(settings.host, settings.db, settings.user, settings.password)
        appointments = db.getAllTodaysAppointments(todayYMD)
        if appointments == []:
            message = "今日の予定はまだないよ。"
        else:
            message = sendAllMsg(appointments, todayHM)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )

    elif "予定を入力" in  msg:
        message = "先頭に'予定'と記載の上，以下の順で予定を入力してください!\n\n場所(e.g:所沢駅)\n日付(e.g: 2017-01-22)\n出発時間(e.g:14:00)\n集合時間(e.g:15:00)\n持ち物(e.g:宿題)" 
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )

    elif ("予定" == msg[:2]) and (len(msg.split("\n")[1:]) == 5):
        results = msg.split("\n")[1:]
        db = usePSQL(settings.host, settings.db, settings.user, settings.password)
        db.updateAppointment(results)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="予定を更新しました")
        )
        
    elif "番の予定を削除" in msg:
        num = msg[0]
        db = usePSQL(settings.host, settings.db, settings.user, settings.password)
        db.delAppointment(num)


    elif "予定を削除" in msg:

        message = "どの予定を削除しますか？\n'1番の予定を削除'のように入力してください\n\n"
        db = usePSQL(settings.host, settings.db, settings.user, settings.password)
        results = sendList(db.getAllDaysAppointments())

        message += results
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )                

    else:
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
