from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('newsapp.urls')),  # Include your app's URLs
   
]