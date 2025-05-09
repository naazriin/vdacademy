from django import forms
from django.utils.translation import gettext_lazy as _
from .models import BlogPost, Comment

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name*'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email*'}),
            'content': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Leave A Comment'
            }),
        }
        labels = {
            'name': 'Name',
            'email': 'Email',
            'content': 'Comment',
        }
