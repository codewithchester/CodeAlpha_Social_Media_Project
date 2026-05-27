from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

# Try to import SignUpView, with fallback
try:
    from posts.views import SignUpView
except ImportError:
    SignUpView = None
    print("SignUpView not found - make sure you added it to posts/views.py")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
]

# Only add signup URL if SignUpView exists
if SignUpView:
    urlpatterns += [
        path('accounts/signup/', SignUpView.as_view(), name='signup'),
    ]

# Add login/logout URLs
urlpatterns += [
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]