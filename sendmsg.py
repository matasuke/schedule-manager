from settings import *
from getStation import * 
from defTimes import *
from connectDB import *

def sendMsg(row, todayHM):
    place = row[0]
    today = str(row[1])
    depart_time = str(row[2])
    appointed_time = str(row[3])
    brings = row[4]

    message1 = place + "にて" + appointed_time[:2] + "時" + appointed_time[3:5]+ "分から予定があります。"
    message2 = "出発予定時刻は" + depart_time[:2]+ "時" + depart_time[3:5] + "分です "
    message3 = "持ち物は" + brings + "です。"

    #if todayHM < row[2]:

    #message5 = "以下に目的地までのルートを記載します。"
    #message6 = Get_Station_info("所沢駅", "小手指駅", "20161221"," 1655")

    messages = message1 + "\n" + message2 + "\n" + message3 # + "\n" + message5  + "\n" + message6

    return messages

def sendAllMsg(rows, todayHM):
    
    messages = ""
    message1 = "本日の予定は以下の通りです。"
    
    for (i,row) in enumerate(rows, start=1):
        messages += "予定" + str(i) + "\n"
        messages += sendMsg(row, todayHM)
        messages += "\n\n"

    message = message1 + "\n\n" + messages

    return message

