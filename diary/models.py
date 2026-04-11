from django.db import models
from core.models import UserProfile

# Create your models here.
class Student(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="student")

    def __str__(self):
        return self.user_profile.user.username

    def total_logics(self):
        return sum(grade.logic_points for grade in self.grades.all())

    def total_money(self):
        return self.total_logics() * 1.5


class Grade(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='grades'
    )
    logic_points = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.logic_points} логік"
