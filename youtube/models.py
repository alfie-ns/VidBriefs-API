from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    # TODO: Add a preferance field that is constantly updated

class Video(models.Model):
    video_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()

class UserInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
