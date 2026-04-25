from django.db import models

# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    publication_date = models.DateTimeField()
    