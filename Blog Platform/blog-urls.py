# Add this line to your existing blog/urls.py file in the urlpatterns list

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # ... your existing URLs ...
    path('', views.HomeView.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    # Add this new URL for markdown preview
    path('preview/', views.markdown_preview, name='markdown_preview'),
]