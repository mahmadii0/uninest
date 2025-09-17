
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('', include('lectures.urls')),
    path('', include('classes.urls')),
    path('',include('exams.urls')),
    path('admin/', admin.site.urls),
]
