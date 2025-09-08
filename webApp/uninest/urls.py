
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('', include('webApp.lectures.urls')),
    path('', include('webApp.classes.urls')),
    path('admin/', admin.site.urls),
]
