from django.contrib import admin
from blog.models import Post, Category, Profile, Comment, Like, FollowUser
# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(FollowUser)