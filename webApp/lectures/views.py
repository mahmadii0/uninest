from django.http import HttpResponse
from django.shortcuts import render
from shared.models import Lecture
from shared import dbMig
from webApp.utils.utils import publishEvent


def addLecture(request,token):
    if request.method=='POST':
        groupID = ""
        rqust= dbMig.getRequest(token)
        groupID=rqust[1]
        if groupID=="":
            print('error while getting groupID')
            return HttpResponse("Bad Request", status=400)
        lecture=Lecture(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            pic=request.POST.get('image'),
            rate=0
        )
        if len(lecture.name)>100 or lecture.name == None:
            print('error in name')
            return HttpResponse("Bad Request", status=400)
        elif len(lecture.phone)>11 or len(lecture.phone)<11:
            print('error in phone')
            return HttpResponse("Bad Request", status=400)
        status= dbMig.addLecture(lecture, groupID)
        if status!=True:
            print('error while adding to database')
            return HttpResponse("Bad Request", status=400)
        status= dbMig.delRequest(token)
        if status!=True:
            print('error while adding to database')
            return HttpResponse("Bad Request", status=400)
        publishEvent("lecture-added", {"groupID": groupID})
        return render(request, 'return-to-bot.html')
    elif request.method=='GET':
        return render(request, 'create-edit-lecture.html', {'typee': 'add'})