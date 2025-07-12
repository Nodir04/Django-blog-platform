"""
Views for the blog application.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Post
from .forms import PostForm
import markdown2

class PostListView(ListView):
    """Homepage view displaying all blog posts."""
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')

class PostDetailView(DetailView):
    """Detail view for individual blog posts."""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    """Create new blog post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update existing blog post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete blog post."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:home')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Authentication views
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

# AJAX view for markdown preview
def markdown_preview(request):
    """Return markdown content as HTML for preview."""
    if request.method == 'POST':
        content = request.POST.get('content', '')
        html = markdown2.markdown(content, extras=['fenced-code-blocks', 'tables'])
        return JsonResponse({'html': html})
    return JsonResponse({'error': 'Invalid request'})