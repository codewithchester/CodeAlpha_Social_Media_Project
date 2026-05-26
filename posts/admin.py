from django.contrib import admin
from .models import Profile, Post, Comment

# Custom admin for Post to show likes count
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'content_preview', 'created_at', 'total_likes']
    search_fields = ['author__username', 'content']
    list_filter = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def total_likes(self, obj):
        return obj.likes.count()
    total_likes.short_description = 'Likes'

# Custom admin for Profile to show followers count
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio_preview', 'created_at', 'total_followers']
    search_fields = ['user__username', 'bio']
    
    def bio_preview(self, obj):
        return obj.bio[:50] + "..." if len(obj.bio) > 50 else obj.bio
    bio_preview.short_description = 'Bio'
    
    def total_followers(self, obj):
        return obj.followers.count()
    total_followers.short_description = 'Followers'

# Register models with custom admin classes
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)