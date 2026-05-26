from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'What\'s on your mind?',
                'rows': 3,
                'class': 'post-input'
            }),
        }