from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

def home(request):
    """Display all posts on the homepage"""
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/home.html', {'posts': posts})

@login_required
def create_post(request):
    """Create a new post"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Don't save to DB yet
            post.author = request.user       # Set current user as author
            post.save()                      # Now save to DB
            return redirect('home')          # Go back to homepage
    else:
        form = PostForm()
    
    return render(request, 'posts/create_post.html', {'form': form})