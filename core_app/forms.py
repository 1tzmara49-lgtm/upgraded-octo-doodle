from django import forms
from .models import Post
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок'
            }),
            'content': forms.Textarea(attrs={
               'class': 'form-control',
                'rows': 5,
                'placeholder': 'О чем вы думаете?'
            }),
        }

class UserProfileForm(forms.ModelForm):
    avatarURL = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'input',
            'placeholder': 'Avatar URL (https://...)'
        }),
        label="Profile picture URL"
    )

    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Username'
            }),
        }