from django.urls import path
from . import views

urlpatterns = [
    # path('classes/', views.classes, name='classes'),
    path('add-lecture/<int:token>/', views.addLecture, name='addLecture'),
    path('edit-lecture/<int:token>/', views.editLecture, name='editLecture'),
]
