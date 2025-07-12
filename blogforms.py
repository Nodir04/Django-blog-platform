"""
Forms for the blog application.
"""
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """Form for creating and editing blog posts."""
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Write your post content in Markdown...'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Technology, Travel, Food'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tags separated by commas'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].help_text = 'Choose a catchy title for your post'
        self.fields['content'].help_text = 'Write your content using Markdown syntax'
        self.fields['category'].help_text = 'Optional: categorize your post'
        self.fields['tags'].help_text = 'Optional: add tags separated by commas'