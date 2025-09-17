from django.urls import path
from . import views

urlpatterns = [
    path('add-exam/<int:token>/', views.addExam, name='addExam'),
    path('edit-exam/<int:token>/',views.editExam, name='editExam')
]
