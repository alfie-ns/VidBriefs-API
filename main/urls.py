# main/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('youtube/', include('youtube.urls')), # youtube app URL
    path('ted_talks/', include('ted_talks.urls')), # ted-talks app URL
    path('admin/', admin.site.urls), # Admin URL
    path('accounts/', include('accounts.urls')), # Accounts app URL
]
