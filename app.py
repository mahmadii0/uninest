import mysql.connector
from contextlib import contextmanager
from constants import connectionDetail,tables
@contextmanager
def dbConnection():
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host=connectionDetail['host'],
            port=connectionDetail['port'],
            user=connectionDetail['user'],
            password=connectionDetail['password'],
            database=connectionDetail['database']
        )
        cursor = conn.cursor()
        conn.autocommit=True
        yield cursor

    except Exception as e:
        print("An error occurred:", e)
        if conn:
            conn.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print('Connection closed')

def createTables():
    with dbConnection() as cursor:
        for table in tables:
            query=tables[table]
            cursor.execute(query)

def getGroupIDs():
    with dbConnection() as cursor:
        query='SELECT groupID FROM botgroups'
        cursor.execute(query)
        list=cursor.fetchall()
        return list

def addGroup(group):
    with dbConnection() as cursor:
        query='INSERT INTO botgroups VALUES(%s,%s,%s)'
        cursor.execute(query,(group.groupID,group.name,group.lang))
        return True