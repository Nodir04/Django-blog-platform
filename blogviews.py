"""
Authentication views for the blog application.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView

def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('blog:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    """Display user profile with their posts."""
    user_posts = request.user.post_set.all().order_by('-created_at')
    return render(request, 'blog/profile.html', {'user_posts': user_posts})

def user_profile(request, username):
    """Display public profile of a specific user."""
    try:
        user = User.objects.get(username=username)
        user_posts = user.post_set.all().order_by('-created_at')
        return render(request, 'blog/user_profile.html', {
            'profile_user': user,
            'user_posts': user_posts
        })
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('blog:home')