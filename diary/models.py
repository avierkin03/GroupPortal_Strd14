from django.db import models
from core.models import UserProfile


class Grade(models.Model):
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='grades'
    )
    logic_points = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile} - {self.logic_points} логік"
