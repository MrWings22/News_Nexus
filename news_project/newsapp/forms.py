from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comments']
        widgets = {
            'comments': forms.Textarea(attrs={
                'class': 'form-control comment-input',  # Bootstrap styling
                'placeholder': 'Write your comment here...',
                'rows': 3,  # Set number of visible lines
                'style': ' border-radius: 10px; padding: 10px; width: 57vh; border: none; '  # Custom CSS styling
            }),
        }