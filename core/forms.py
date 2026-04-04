from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

# Форма реєстації нових користувачів
class SignUpForm(UserCreationForm):
    bio = forms.CharField(
        label='Біографія',
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False
    )
    avatar = forms.ImageField(label='Аватар', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'bio', 'avatar']

    def save(self, commit=True):
        user = super().save(commit=True) 
        if commit:
            if not UserProfile.objects.filter(user=user).exists():
                UserProfile.objects.create(
                    user=user,
                    bio=self.cleaned_data['bio'],
                    avatar=self.cleaned_data['avatar'],
                    role='member'
                )
            else:
                profile = user.profile
                profile.bio = self.cleaned_data['bio']
                if self.cleaned_data['avatar']:
                    profile.avatar = self.cleaned_data['avatar']
                profile.save()
        return user