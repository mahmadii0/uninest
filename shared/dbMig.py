import mysql.connector
from contextlib import contextmanager
from .constants import connectionDetail,tables


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

def addRequest(token,groupID,typee):
    with dbConnection() as cursor:
        query='INSERT INTO requests VALUES (%s,%s,%s)'
        cursor.execute(query,(token,int(groupID),typee,))
    return True
def getRequest(token):
    with dbConnection() as cursor:
        query='SELECT * FROM requests WHERE token=%s'
        cursor.execute(query,(token,))
        request=cursor.fetchone()
        return request
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

def getLecture(lecID,groupID):
    with dbConnection() as cursor:
        query='SELECT * FROM lectures WHERE lecID=%s AND groupID=%s'
        cursor.execute(query,(lecID,groupID,))
        lecture=cursor.fetchone()
        return lecture

def getAllLecture(groupID):
    with dbConnection() as cursor:
        query='SELECT * FROM lectures WHERE groupID=%s'
        cursor.execute(query,(groupID,))
        list=cursor.fetchall()
        return list

def editLecture(lecture,groupID):
    with dbConnection() as cursor:
        query='UPDATE lectures SET lec_name=%s, phone=%s, rate=%s, pic=%s WHERE lecID=%s and groupID=%s'
        cursor.execute(query,(lecture.name,lecture.phone,float(lecture.rate),lecture.pic,lecture.lecID,groupID,))
        return True

def deleteLecture(lecID,groupID):
    with dbConnection() as cursor:
        query='DELETE FROM lectures WHERE lecID=%s and groupID=%s'
        cursor.execute(query,(lecID,groupID,))
        return True

#Class
def addClass(clss,groupID):
    with dbConnection() as cursor:
        query='INSERT INTO classes(class_name,lecID,groupID) VALUES(%s,%s,%s)'
        cursor.execute(query,(clss.name,clss.lecID,groupID,))
        return True
def getClass(clssID,groupID):
    with dbConnection() as cursor:
        query='SELECT * FROM classes WHERE classID=%s AND groupID=%s'
        cursor.execute(query,(clssID,groupID,))
        clss=cursor.fetchone()
        return clss
def getAllClass(groupID):
    with dbConnection() as cursor:
        query='SELECT * FROM classes WHERE groupID=%s'
        cursor.execute(query,(groupID,))
        list=cursor.fetchall()
        return list
def editClass(clss,groupID):
    with dbConnection() as cursor:
        query='UPDATE classes SET class_name=%s, lecID=%s WHERE classID=%s and groupID=%s'
        cursor.execute(query,(clss.name,clss.lecID,clss.classID,groupID,))
        return True
def deleteClass(clssID,groupID):
    with dbConnection() as cursor:
        with dbConnection() as cursor:
            query = 'DELETE FROM classes WHERE classID=%s and groupID=%s'
            cursor.execute(query, (clssID, groupID,))
            return True
#Student
def addStudent(student,groupID):
    with dbConnection() as cursor:
        query='INSERT IGNORE INTO students(studentID,std_name,username,groupID) VALUES(%s,%s,%s,%s)'
        cursor.execute(query,(student.StudentID,student.name,student.username,groupID,))
        return True

def addStudentToClass(studentID,classID,groupID):
    with dbConnection() as cursor:
        query='INSERT INTO student_class_relation(classID,studentID,groupID) VALUES(%s,%s,%s)'
        cursor.execute(query,(classID,studentID,groupID))
        return True

def getStudent(studentID,classID,groupID):
    with dbConnection() as cursor:
        query='SELECT classID FROM student_class_relation WHERE studentID=%s AND groupID=%s AND classID=%s'
        cursor.execute(query,(studentID,groupID,classID,))
        std=cursor.fetchone()
        return std
def getAllStudent(classID,groupID):
    with dbConnection() as cursor:
        query='''SELECT students.std_name, students.username FROM student_class_relation INNER JOIN students ON student_class_relation.studentID=students.studentID WHERE student_class_relation.classID=%s and student_class_relation.groupID=%s'''
        cursor.execute(query,(classID,groupID,))
        list=cursor.fetchall()
        return list
def editStudent(student,groupID):
    with dbConnection() as cursor:
        query='UPDATE students SET std_name=%s, username=%s WHERE studentID=%s and groupID=%s'
        cursor.execute(query,(student.name,student.username,student.StudentID,groupID,))
        return True
def deleteStudent(studentID,classID,groupID):
    with dbConnection() as cursor:
        query = 'DELETE FROM student_class_relation WHERE studentID=%s and groupID=%s and classID=%s'
        cursor.execute(query, (studentID, groupID,classID))
        return True
#Exam
def addExam(exam):
    with dbConnection() as cursor:
        query='INSERT INTO exams(title,classID,date_time) VALUES(%s,%s,%s)'
        cursor.execute(query,(exam.title,exam.classID,exam.dateTime,))
        return True

def editExam(exam,examID):
    with dbConnection() as cursor:
        query='UPDATE exams SET title=%s, date_time=%s WHERE examID=%s'
        cursor.execute(query,(exam.title,exam.dateTime,examID,))
        return True

def getExams(classID):
    with dbConnection() as cursor:
        query='SELECT * FROM exams WHERE classID=%s'
        cursor.execute(query,(classID,))
        list=cursor.fetchall()
        return list

def getExam(examID):
    with dbConnection() as cursor:
        query = 'SELECT * FROM exams WHERE examID=%s'
        cursor.execute(query, (examID,))
        std = cursor.fetchone()
        return std

def deleteExam(examID):
    with dbConnection() as cursor:
        query = 'DELETE FROM exams WHERE examID=%s'
        cursor.execute(query, (examID,))
        return True

def addFile(file):
    with dbConnection() as cursor:
        query='INSERT INTO files VALUES(%s,%s,%s)'
        cursor.execute(query,(file.FileName,file.address,file.classID,))
        return True

def getFile(fileName,classID):
    with dbConnection() as cursor:
        query='SELECT * FROM files WHERE file_name=%s and classID=%s'
        cursor.execute(query,(fileName,classID,))
        file=cursor.fetchone()
        return file

def deleteFile(fileName,classID):
    with dbConnection() as cursor:
        query='DELETE FROM files WHERE file_name=%s and classID=%s'
        cursor.execute(query,(fileName,classID,))
        return True
