from getStation import * 

def SendMsg(row, todayHM):
    place = row[0]
    today = str(row[1])
    depart_time = str(row[2])
    appointed_time = str(row[3])
    brings = row[4]

    appointed_time = str(row['appointed_time'])[11:]
    depart_time = str(row['depart_time'])[11:]
    station = row['station']

    message1 = "本日の予定は以下の通りです"
    message2 = place + "にて" + appointed_time[:2] + "時" + appointed_time[3:5]+ "分から予定があります。"
    message3 = "出発予定時刻は" + depart_time[:2]+ "時" + depart_time[3:5] + "分です "
    message4 = "持ち物は" + brings + "です。"

    #now = datetime.datetime.now()
    #if todayHM < row[2]:

    #message5 = "以下に目的地までのルートを記載します。"
    #message6 = Get_Station_info("所沢駅", "小手指駅", "20161221"," 1655")

    messages = message1 + "\n" + message2 + "\n" + message3 + "\n" + message4# + "\n" + message5  + "\n" + message6

    return messages
