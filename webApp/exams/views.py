from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from shared import dbMig
from shared.models import Exam
from webApp.utils.utils import publishEvent


def addExam(request,token):
    if request.method=='POST':
        groupID = ""
        rqust= dbMig.getRequest(token)
        groupID=rqust[1]
        if groupID=="":
            print('error while getting groupID')
            return HttpResponse("Bad Request", status=400)
        exam=Exam(
            title=request.POST.get('title'),
            dateTime=request.POST.get('datetime'),
            classID=token
        )
        if len(exam.title)>100 or exam.title == None:
            print('error in title')
            return HttpResponse("Bad Request", status=400)
        status= dbMig.addExam(exam)
        if status!=True:
            print('error while adding to database')
            return HttpResponse("Bad Request", status=400)
        status= dbMig.delRequest(token)
        if status!=True:
            print('error while deleting request')
            return HttpResponse("Bad Request", status=400)
        publishEvent("exam-added", {"groupID": groupID})
        return render(request, 'return-to-bot.html')
    elif request.method=='GET':
        rqust=dbMig.getRequest(token)
        if rqust == None:
            print("Error while getting request")
            return HttpResponse("Bad request",status=400)
        return render(request, 'create-edit-exam.html', {'typee': 'add'})

def editExam(request, token):
        if request.method == "POST":
            groupID = ""
            rqust = dbMig.getRequest(token)
            groupID = rqust[1]
            if groupID == "":
                print('error while getting groupID')
                return HttpResponse("Bad Request", status=400)
            exam = Exam(
                title=request.POST.get('title'),
                classID=0,
                dateTime=request.POST.get('datetime')
            )
            if len(exam.title) > 100 or exam.title == None:
                print('error in title')
                return HttpResponse("Bad Request", status=400)
            status = dbMig.editExam(exam, token)
            if status != True:
                print('error while adding to database')
                return HttpResponse("Bad Request", status=400)
            status = dbMig.delRequest(token)
            if status != True:
                print('error while deleting request')
                return HttpResponse("Bad Request", status=400)
            publishEvent("exam-edited", {"groupID": groupID})
            return render(request, 'return-to-bot.html')
        elif request.method == "GET":
            rqust = dbMig.getRequest(token)
            if rqust == None:
                print("Error while getting request")
                return HttpResponse("Bad request", status=400)
            exam = dbMig.getExam(token)
            if exam == None:
                print("Error while getting exam")
                return HttpResponse("Bad request", status=400)
            return render(request, 'create-edit-exam.html', {'typee': 'edit', 'exam_title':exam[1],'exam_datetime':exam[3]})