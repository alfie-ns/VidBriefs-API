from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('youtube/', include('youtube.urls')), # youtube URL
    path('ted_talks/', include('ted_talks.urls')),
    path('admin/', admin.site.urls), # Admin URL
]
