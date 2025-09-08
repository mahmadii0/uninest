class Group:
    def __init__(self,groupID:int,name:str,lang:str):
        self.groupID=groupID
        self.name=name
        self.lang=lang
_idCounter=1
class Lecture:
    def __init__(self,name,phone,rate,pic):
        global _idCounter
        self.lecID=_idCounter
        _idCounter+=1
        self.name=name
        self.phone=phone
        self.rate=rate
        self.pic=pic

class Class:
    def __init__(self,name,lecID):
        global _idCounter
        self.lecID = _idCounter
        _idCounter += 1
        self.name=name
        self.lecID=lecID

class Student:
    def __init__(self,name,userName):
        global _idCounter
        self.lecID = _idCounter
        _idCounter += 1
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

