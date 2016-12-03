import pymysql
import settings


def connectDB():
    dbh= pymysql.connect(
        host = settings.host,
        db = settings.db,
        user = settings.user,
        password = settings.password,
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )

    stmt = dbh.cursor() 

    return dbh, stmt


