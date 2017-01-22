import psycopg2
import settings
from defTimes import *

class usePSQL:

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

        self.connector = psycopg2.connect(
                host = self.host,
                database = self.database,
                user = self.user,
                password = self.password
                )
    
        self.cursor = self.connector.cursor()

    def updateSQL(self, sentence):
        self.cursor.execute(sentence)
        self.connector.commit()

    def selectSQL(self, sentence):
        self.cursor.execute(sentence)
        result = self.cursor.fetchall()
    
        return result

    def closeSQL(self):
        self.cursor.close()
        self.connector.close()

    def getAllAppointments(self, todayHM, todayYMD):
        sql = "select * from appointments where day = " + "'" + todayYMD + "'" + "and appointed_time >" + "'" +  todayHM + "'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        
        return result

    def getAllTodaysAppointments(self, todayYMD):
        sql = "select * from appointments where day =" + "'" + todayYMD + "'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        return result

    def updateAppointment(self, results):
        place = results[0]
        day = results[1]
        depart_time = results[2]
        appointed_time = results[3]
        brings = results[4]

        todayHM, todayYMD = getNowTimes()

        if day == "今日":
            day = todayYMD

        sql = "insert into appointments values('" + place +"' , '" + day + "' , '" + depart_time + "' , '" + appointed_time + "' , '" + brings + "')"

        self.cursor.execute(sql)
        self.connector.commit()

    def getAllDaysAppointments(self):
        sql = "select * from appointments"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()

        return results

    def delAppointment(self, num):
        result = getAllDaysAppointments()

        n = int(num) - 1

        delData = result[n]
        place = delData[0]
        day = delData[1]
        depart_time = delData[2]
        appointed_time = delData[3]
        brings = delData[4]

        sql = "delete from appointments where place = '" + place + "' , '" + day + "' , '" + depart_time + "' , '" + appointed_time + "' , '" + brings + "'"

        self.cursor.execute(sql)
        self.connector.commit()
