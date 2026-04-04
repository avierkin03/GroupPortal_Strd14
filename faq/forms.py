from django.forms import forms,ModelForm
from .models import FAQ_model

class FAQ_Form(ModelForm):
    class Meta:
        model = FAQ_model
        fields = ['title','text','answer','status','category']