from django import forms
from .models import Post, Comment

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
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write a comment...',
                'rows': 2,
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
            }),
        }