from django.db import models
from django.contrib.auth.models import User

# Create your models here
class FAQ_model(models.Model):

    STATUS_CHOICES =[
        ('inprogress','In Progress'),
        ('done','Done')]
    CATEGORY_CHOISES =[
        ('food','Food'),
        ('sport','Sport'),
        ('life','Life'),
        ('video','Video'),
        ('site','Site'),
        ('games','Games'),
        ('interestings','Interestings'),
        ('fellings','Fellings'),
        ('other','Other')

    ]

    title = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    answer = models.CharField(max_length=250)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES)
    category = models.CharField(max_length=20,choices=CATEGORY_CHOISES,null=True)
    Questioner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='tasks')