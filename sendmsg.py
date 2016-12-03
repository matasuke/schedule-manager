from getStation import * 


def SendMsg(row):
    appointed_time = str(row['appointed_time'])[11:]
    brings = row['brings']
    place = row['place']
    depart_time = str(row['depart_time'])[11:]
    station = row['station']

    message1 = "本日の予定は以下の通りです"
    message2 = place + "にて" + appointed_time + "時から用事があります。"
    message3 = "出発予定時刻は" + depart_time + "です"
    message4 = "持ち物は" + brings + "です。"
    message5 = "以下に目的地までのルートを記載します。"
    message6 = Get_Station_info("所沢駅", "高田馬場駅", 20161221, 1655)

    messages = message1 + "\n" + message2 + "\n" + message3 + "\n" + message4 + "\n" + message5 + "\n" + message6

    return messages
