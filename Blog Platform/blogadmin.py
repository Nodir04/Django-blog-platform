"""
Admin configuration for the blog application.
"""
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for Post model."""
    list_display = ('title', 'author', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'author')
    search_fields = ('title', 'content', 'tags')
    prepopulated_fields = {'category': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author')
        }),
        ('Categorization', {
            'fields': ('category', 'tags'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )