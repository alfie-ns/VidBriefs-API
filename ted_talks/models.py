# ted_talks/models.py

from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings

# --------------------------------------------------------------
# TED Talk model [ ] 
class TedTalk(models.Model):
    title = models.CharField(max_length=255)        # Title of the talk
    type_of_talk = models.CharField(max_length=255) # Type of the talk, this is generated...
    transcript = models.TextField()               # Transcript of the talk
    keywords = models.TextField()                # Keywords of the talk

    def __str__(self):  # Method to return the title of the talk
        return self.title 

# --------------------------------------------------------------   
# UserWatchedTalk model [ ] 
class UserWatchedTalk(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    talk = models.ForeignKey(TedTalk, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'talk')

# --------------------------------------------------------------
# APIToken model [ ] 
#class APIToken(models.Model):
#    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#    created_at = models.DateTimeField(auto_now_add=True)
#
#    def __str__(self):
#        return f"Token for {self.user.username}"