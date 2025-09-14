from django.urls import path
from . import views

urlpatterns = [
    path('add-class/<int:token>/', views.addClass, name='addClass'),
    path('edit-class/<int:token>/', views.editClass, name='editClass'),
]
