from django import forms
from .models import Announcement

class TaskForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title","description","publication_date"]