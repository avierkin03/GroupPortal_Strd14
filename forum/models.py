from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Forum(models.Model):
    comments = [

    ] #TODO array of comments
    img = models.ImageField()#TODO
    text = models.TextField
    title = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forums")#TODO
    creation_data = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):

    img = models.ImageField()#TODO
    like_counter = models.IntegerField()
    dislike_counter = models.IntegerField()
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forums")#TODO
    creation_data = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)



