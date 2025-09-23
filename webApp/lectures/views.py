import os
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render
from bot import utils
from shared.models import Lecture
from shared import dbMig
from webApp.uninest import settings
from webApp.utils.utils import publishEvent

randnums=[]

def addLecture(request,token):
    if request.method=='POST':
        groupID = ""
        rqust= dbMig.getRequest(token)
        groupID=rqust[1]
        if groupID=="":
            print('error while getting groupID')
            return HttpResponse("Bad Request", status=400)

        pic = request.FILES.get('image')
        picPath = None
        if pic:
            save_dir = os.path.join(settings.MEDIA_ROOT, 'lectures')
            os.makedirs(save_dir, exist_ok=True)
            _num=utils.rand(randnums)
            i = 0
            while i < len(pic.name):
                if pic.name[i] == '.' and pic.name[i + 1] == 'p' and pic.name[i+2]== 'n':
                    pic.name = pic.name[:i] + str(_num) + pic.name[i:]
                    break
                elif pic.name[i] == '.' and pic.name[i + 1] == 'j' and pic.name[i+2]== 'g':
                    pic.name = pic.name[:i] + str(_num) + pic.name[i:]
                    break
                i += 1
            picPath = os.path.join(save_dir, pic.name)

            # save file to disk
            with default_storage.open(picPath, 'wb+') as dest:
                for chunk in pic.chunks():
                    dest.write(chunk)

            # relative path for DB
            picPath = f'lectures\\{pic.name}'

        else:
            picPath=""
        lecture=Lecture(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            pic=picPath,
            rate=0
        )
        if len(lecture.name)>100 or lecture.name == None:
            print('error in name')
            return HttpResponse("Bad Request", status=400)
        elif len(lecture.phone)>11:
            print('error in phone')
            return HttpResponse("Bad Request", status=400)
        status= dbMig.addLecture(lecture, groupID)
        if status!=True:
            print('error while adding to database')
            return HttpResponse("Bad Request", status=400)
        status= dbMig.delRequest(token)
        if status!=True:
            print('error while deleting request')
            return HttpResponse("Bad Request", status=400)
        publishEvent("lecture-added", {"groupID": groupID})
        return render(request, 'return-to-bot.html')
    elif request.method=='GET':
        return render(request, 'create-edit-lecture.html', {'typee': 'add'})

def editLecture(request,token):
    if request.method=="POST":
        groupID = ""
        rqust= dbMig.getRequest(token)
        groupID=rqust[1]
        if groupID=="":
            print('error while getting groupID')
            return HttpResponse("Bad Request", status=400)
        pic = request.FILES.get('image')
        picPath = None
        if pic:
            save_dir = os.path.join(settings.MEDIA_ROOT, 'lectures')
            os.makedirs(save_dir, exist_ok=True)
            _num=utils.rand(randnums)
            i = 0
            while i < len(pic.name):
                if pic.name[i] == '.' and pic.name[i + 1] == 'p' and pic.name[i+2]== 'n':
                    pic.name = pic.name[:i] + str(_num) + pic.name[i:]
                    break
                elif pic.name[i] == '.' and pic.name[i + 1] == 'j' and pic.name[i+2]== 'g':
                    pic.name = pic.name[:i] + str(_num) + pic.name[i:]
                    break
                i += 1
            picPath = os.path.join(save_dir, pic.name)

            # save file to disk
            with default_storage.open(picPath, 'wb+') as dest:
                for chunk in pic.chunks():
                    dest.write(chunk)

            # relative path for DB
            picPath = f'lectures\\{pic.name}'
        else:
            picPath=""
        lecture=Lecture(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            pic=picPath,
            rate=request.POST.get('rate')
        )
        i=0
        while i<len(lecture.phone):
            if lecture.phone[i] == ' ':
                if i==0:
                    lecture.phone=lecture.phone[i+1:]
                else:
                    lecture.phone=lecture.phone[:i]+lecture.phone[i+1:]
            i+=1

        lecture.lecID=token
        oldPic=dbMig.getPicLecture(lecture.lecID,groupID)
        oldPicPath=os.path.join(settings.MEDIA_ROOT,oldPic[0])
        if os.path.exists(oldPicPath):
            os.remove(oldPicPath)

        if len(lecture.name)>100 or lecture.name == None:
            print('error in name')
            return HttpResponse("Bad Request", status=400)
        elif len(lecture.phone)>11:
            print('error in phone')
            return HttpResponse("Bad Request", status=400)
        status= dbMig.editLecture(lecture, groupID)
        if status!=True:
            print('error while adding to database')
            return HttpResponse("Bad Request", status=400)
        status= dbMig.delRequest(token)
        if status!=True:
            print('error while deleting request')
            return HttpResponse("Bad Request", status=400)
        publishEvent("lecture-edited", {"groupID": groupID})
        return render(request, 'return-to-bot.html')
    elif request.method=="GET":
        groupID = ""
        rqust=dbMig.getRequest(token)
        groupID=rqust[1]
        if groupID=="":
            print("Error while getting groupID")
            return HttpResponse("Bad Request",status=400)
        lec = dbMig.getLecture(token,groupID)
        if lec == None:
            print("Error while getting lecture")
            return HttpResponse("Bad Request",status=400)
        return render(request,'create-edit-lecture.html',{'typee':'edit','lec_name':lec[1],'lec_phone':lec[2],'lec_rate':lec[3]})