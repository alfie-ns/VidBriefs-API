from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('response/', include('response.urls')),
]
