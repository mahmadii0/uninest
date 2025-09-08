import mysql.connector
from contextlib import contextmanager
from constants import connectionDetail,tables
import lecture
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
#Group
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

def addRequest(token,groupID):
    with dbConnection() as cursor:
        query='INSERT INTO requests VALUES (%s,%s)'
        cursor.execute(query,(token,int(groupID)))
    return True
def getRequest(token):
    with dbConnection() as cursor:
        query='SELECT groupID FROM requests WHERE token=%s'
        cursor.execute(query,(token,))
        id=cursor.fetchone()
        return id[0]
def delRequest(token):
    with dbConnection() as cursor:
        query='DELETE FROM requests WHERE token=%s'
        cursor.execute(query,(token,))
    return True


#Lecture
def addLecture(lecture,groupID):
    with dbConnection() as cursor:
        query='INSERT INTO lectures(lec_name,phone,rate,pic,groupID) VALUES(%s,%s,%s,%s,%s)'
        cursor.execute(query,(lecture.name,lecture.phone,lecture.rate,lecture.pic,groupID))
    return True
