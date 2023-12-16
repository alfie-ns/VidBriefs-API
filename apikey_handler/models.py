from django.db import models
import os

# Create your models here.

class ApiKey(models.Model):
    key = os.environ.get('OPENAI_API_KEY')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)
    usage_count = models.IntegerField(default=0)

    def __str__(self):
        return self.key
