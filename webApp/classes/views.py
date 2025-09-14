from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from shared import dbMig
from shared.models import Lecture,Class
from webApp.utils.utils import publishEvent


def addClass(request,token):
    if request.method=='POST':
        groupID = ""
        rqust= dbMig.getRequest(token)
        groupID=rqust[1]
        if groupID=="":
            print('error while getting groupID')
            return HttpResponse("Bad Request", status=400)
        clss=Class(
            name=request.POST.get('name'),
            lecID=request.POST.get('lecture')
        )
        if len(clss.name)>100 or clss.name == None:
            print('error in name')
            return HttpResponse("Bad Request", status=400)
        status= dbMig.addClass(clss,groupID)
        if status!=True:
            print('error while adding to database')
            return HttpResponse("Bad Request", status=400)
        status= dbMig.delRequest(token)
        if status!=True:
            print('error while deleting request')
            return HttpResponse("Bad Request", status=400)
        publishEvent("class-added", {"groupID": groupID})
        return render(request, 'return-to-bot.html')
    elif request.method=='GET':
        rqust=dbMig.getRequest(token)
        if rqust == None:
            print("Error while getting request")
            return HttpResponse("Bad request",status=400)
        lectures=dbMig.getAllLecture(rqust[1])
        list=[]
        for lec in lectures:
            lecture=Lecture(
                name=lec[1],
                phone=lec[2],
                rate=lec[3],
                pic=''
            )
            lecture.lecID=lec[0]
            list.append(lecture)
        return render(request, 'create-edit-class.html', {'typee': 'add','lectures':list})

def editClass(request,token):
    if request.method=="POST":
        groupID = ""
        rqust = dbMig.getRequest(token)
        groupID = rqust[1]
        if groupID == "":
            print('error while getting groupID')
            return HttpResponse("Bad Request", status=400)
        clss = Class(
            name=request.POST.get('name'),
            lecID=request.POST.get('lecture')
        )
        clss.classID=token
        if len(clss.name) > 100 or clss.name == None:
            print('error in name')
            return HttpResponse("Bad Request", status=400)
        status = dbMig.editClass(clss, groupID)
        if status != True:
            print('error while adding to database')
            return HttpResponse("Bad Request", status=400)
        status = dbMig.delRequest(token)
        if status != True:
            print('error while deleting request')
            return HttpResponse("Bad Request", status=400)
        publishEvent("class-edited", {"groupID": groupID})
        return render(request, 'return-to-bot.html')
    elif request.method=="GET":
        rqust=dbMig.getRequest(token)
        if rqust == None:
            print("Error while getting request")
            return HttpResponse("Bad request",status=400)
        clss=dbMig.getClass(token,rqust[1])
        if clss==None:
            print("Error while getting class")
            return HttpResponse("Bad request",status=400)
        lectures=dbMig.getAllLecture(rqust[1])
        list=[]
        for lec in lectures:
            lecture=Lecture(
                name=lec[1],
                phone=lec[2],
                rate=lec[3],
                pic=''
            )
            lecture.lecID=lec[0]
            list.append(lecture)
        return render(request, 'create-edit-class.html', {'typee': 'edit','lectures':list,'class_name':clss[1]})