from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Forum(models.Model):
    img = models.ImageField(upload_to='forum_images/', blank=True, null=True)
    text = models.TextField()
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forums")
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-creation_date']


class Comment(models.Model):

    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="comments")

    img = models.ImageField(upload_to='comment_images/', blank=True, null=True)
    like_counter = models.IntegerField(default=0)
    dislike_counter = models.IntegerField(default=0)
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.owner.username}"

    class Meta:
        ordering = ['-creation_date']


