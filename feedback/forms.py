from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'message', 'rating']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }