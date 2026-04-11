from django.forms import forms,ModelForm
from .models import FAQ_model

class FAQ_Form_UPD(ModelForm):
    class Meta:
        model = FAQ_model
        fields = ['title','text','answer','status','category']

class FAQ_Form_CRT(ModelForm):
    class Meta:
        model = FAQ_model
        fields = ['title','text','category']