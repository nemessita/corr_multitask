from django.contrib import admin
from django.urls import path
from main.views import index, home, exc

urlpatterns = [
    
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('exc/', exc, name='exc'),

]

