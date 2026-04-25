from django import forms
from .models import Forum, Comment

# Форма для створення/редагування задач
class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ["img", "title", "text"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["img", "text"]
