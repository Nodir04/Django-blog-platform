"""
Blog models for the blog application.
"""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import markdown2

class Post(models.Model):
    """Blog post model with Markdown support."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Optional: Add categories/tags
    category = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """Return the URL for this post."""
        return reverse('blog:post_detail', kwargs={'pk': self.pk})
    
    def get_markdown_content(self):
        """Convert markdown content to HTML."""
        return markdown2.markdown(self.content, extras=['fenced-code-blocks', 'tables'])
    
    def get_tags_list(self):
        """Return tags as a list."""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def get_snippet(self, length=150):
        """Return a snippet of the post content."""
        if len(self.content) <= length:
            return self.content
        return self.content[:length] + '...'