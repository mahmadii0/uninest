from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse

def classes(request):
    pass

def addClass(request):
    if request.method=='POST':
        return HttpResponse('lll')
    elif request.method=='GET':
        return render(request, 'create-edit-class.html', {'typee': 'add'})