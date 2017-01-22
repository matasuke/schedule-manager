import psycopg2
import settings


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
