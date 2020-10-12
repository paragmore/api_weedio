from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils import timezone

# Create your models here.

class Platform(models.Model):
    platformName= models.CharField(max_length=50)

    def __str__(self):
        return self.platformName

class Channel(models.Model):
    channelName= models.CharField(max_length=25)
    
    def __str__(self):
        return self.channelName

class Video(models.Model):
    videoId= models.CharField(max_length=200,unique=True)
    caption= models.TextField(max_length=300)
    channel= models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos')
    platform= models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='videos', default= None)
    start=models.CharField(max_length=200, null=True,blank=True, default=None)
    end= models.CharField(max_length=200, null=True,blank=True, default=None)
    tags = TaggableManager()
    
    def __str__(self):
        return self.caption

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes',null=True)
    date_created = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Like, self).save(*args, **kwargs)

class Dislike(models.Model):
    disliker = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='dislikes',null=True)
    date_created = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Dislike, self).save(*args, **kwargs)

class Watched(models.Model):
    videoId= models.CharField( max_length=200)
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ip= models.CharField(max_length=300,null=True)

    def __str__(self):
        return self.videoId

class Browser(models.Model):
    videoId= models.CharField( max_length=200)
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ip= models.CharField(max_length=300,null=True)
    timestamp= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.videoId