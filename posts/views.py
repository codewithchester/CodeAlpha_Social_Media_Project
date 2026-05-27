from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Post, Comment, Profile
from .forms import PostForm, CommentForm


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


def profile(request, username):
    """Display a user's profile page"""
    # Get the user or show 404 error if not found
    user_profile = get_object_or_404(User, username=username)
    
    # Get all posts by this user
    user_posts = Post.objects.filter(author=user_profile).order_by('-created_at')
    
    # Get or create profile (in case profile doesn't exist)
    profile, created = Profile.objects.get_or_create(user=user_profile)
    
    # Check if current user follows this profile (only if logged in)
    is_following = False
    if request.user.is_authenticated and request.user != user_profile:
        is_following = profile.followers.filter(id=request.user.id).exists()
    
    context = {
        'profile_user': user_profile,
        'profile': profile,
        'posts': user_posts,
        'is_following': is_following,
    }
    
    return render(request, 'posts/profile.html', context)


# ADD THESE FUNCTIONS
@login_required
def follow_user(request, username):
    """Follow a user"""
    user_to_follow = get_object_or_404(User, username=username)
    
    # Can't follow yourself
    if request.user != user_to_follow:
        user_to_follow.profile.followers.add(request.user)
    
    return redirect('profile', username=username)

@login_required
def unfollow_user(request, username):
    """Unfollow a user"""
    user_to_unfollow = get_object_or_404(User, username=username)
    
    # Can't unfollow yourself
    if request.user != user_to_unfollow:
        user_to_unfollow.profile.followers.remove(request.user)
    
    return redirect('profile', username=username)


@login_required
def add_comment(request, post_id):
    """Add a comment to a post"""
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
            messages.success(request, 'Comment added!')
    
    # Go back to the page user came from
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def like_post(request, post_id):
    """Like or unlike a post"""
    post = get_object_or_404(Post, id=post_id)
    
    # Check if user already liked this post
    if request.user in post.likes.all():
        # Unlike: remove the like
        post.likes.remove(request.user)
        messages.success(request, 'You unliked this post')
    else:
        # Like: add the like
        post.likes.add(request.user)
        messages.success(request, 'You liked this post!')
    
    # Go back to the page user came from
    return redirect(request.META.get('HTTP_REFERER', 'home'))



class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'