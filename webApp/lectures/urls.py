from django.urls import path
from . import views

urlpatterns = [
    # path('classes/', views.classes, name='classes'),
    path('add-lecture/<int:token>/', views.addLecture, name='addLecture'),
    # path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
    # path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
]
