import sys
import requests
from bs4 import BeautifulSoup

def Get_Station_info(fro, to, when, time):
    
    year = when[:4]
    month = when[4:6]
    day = when[6:8]
    hour = time[:2]
    minit1 = time[2:3]
    minit2 = time[3:4]

    
    #list
    st_name = []
    t_list = []
    train_names = []
    
    #get url
    URL_BASE = "http://transit.yahoo.co.jp/search/result?flatlon=&from=" + str(fro) + "&tlatlon=&to=" + str(to) + "&via=&via=&via=&y=" + str(year) + "&m=" + str(month) + "&d=" + str(day) + "&hh=" + str(hour) + "&m2=" + str(minit2) + "&m1=" + str(minit1) + "&type=1&ticket=ic&al=1&shin=1&ex=1&hb=1&lb=1&sr=1&s=0&expkind=1&ws=3"

    r = requests.get(URL_BASE)
    soup = BeautifulSoup(r.content)

    stations = soup.find(id="route01").find(class_="routeDetail")
    
    #get station name
    dt = stations.find_all("dt")
    soup2 = BeautifulSoup(str(dt))
    urls = soup2.find_all("a")

    for i in urls:
        st_name.append(i.text)

    #get time
    times = stations.find_all("ul", class_="time")
    for t in times:
        t_list.append(t.text)

    #get train name
    trains = stations.find_all("li", class_="transport")
    for train in trains:
        train_names.append(train.text[16:])


    message1 = st_name[0] +  "から" + st_name[-1] + "への経路"
    message2 = t_list[0] + "時に" + st_name[0] + "駅からの電車があります。"
    message3 = st_name[0] + "から" + t_list[0] + "時発の" + train_names[0][:13] + "に乗車して" + st_name[1] + "に向かって下さい。"
    message4 = t_list[-1] + "時に到着予定です。"

    messages = message1 + "\n" + message2 + "\n" + message3 + "\n" + message4

    return messages

if __name__ == "__main__":
    
    args = sys.argv
    argc = len(args)
    fro = args[1]
    to = args[2]
    when = args[3]
    time = args[4]

    if argc != 5:
        print("USAGE: python get_statin_name.py [from] [to] [when] [time]")
        print("example python get_statin_name.py 新宿駅 東京駅 20161203 1644")
    messages = Get_Station_info(fro, to, when, time)
    print(messages)
