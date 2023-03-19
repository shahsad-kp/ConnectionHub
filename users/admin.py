from django.contrib import admin

from .models import User, Follow, Blocks, FollowRequest

admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Blocks)
admin.site.register(FollowRequest)