class Lecture:
    def __init__(self,lecID,name,phone,rate,pic):
        self.lecID=lecID
        self.name=name
        self.phone=phone
        self.rate=rate
        self.pic=pic

class Class:
    def __init__(self,classID,name,lecID):
        self.classID=classID
        self.name=name
        self.lecID=lecID

class Student:
    def __init__(self,studentID,name,userName):
        self.studentID=studentID
        self.name=name
        self.username=userName

class File:
    def __init__(self,address,classID):
        self.address=address
        self.classID=classID

class Exam:
    def __init__(self,title,classID,dateTime):
        self.title=title
        self.classID=classID
        self.dateTime=dateTime

