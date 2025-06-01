from django.contrib import admin

from ramailo.models.feedback import Feedback
from ramailo.models.notification import FCMDevice
from ramailo.models.user import User
from ramailo.models.post import Post,Comment,Category,PostImage


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'idx', 'mobile', 'name', 'position', 'created_at']
    search_fields = ['name', 'mobile']
    list_filter = ['is_approved', 'is_email_verified', 'is_kyc_verified']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','idx', 'title', 'author', 'is_published', 'created_at']
    search_fields = ['title', 'author__name']
    list_filter = ['is_published']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id' ,'idx' ,'user', 'post', 'created_at']
    search_fields = ['user__name', 'post__title']
    list_filter = ['post']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['idx','name']
    search_fields = ['name']
    list_filter = ['name']

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'url']


admin.site.register(FCMDevice)
