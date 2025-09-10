from django.urls import path
from . import views

urlpatterns = [
    path('add-class/<int:token>/', views.addClass, name='addClass'),
    # path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
    # path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
]
