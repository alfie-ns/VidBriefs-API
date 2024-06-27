# ted_talks/models.py

from django.db import models

class TedTalk(models.Model):
    title = models.CharField(max_length=255)
    type_of_talk = models.CharField(max_length=255)
    transcript = models.TextField()
    keywords = models.TextField()

    def __str__(self):
        return self.title