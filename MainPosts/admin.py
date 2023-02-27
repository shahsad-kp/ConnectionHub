from django.contrib import admin

from .models import Post, Reaction, Comment, Tag, SavedPost

admin.site.register(Post)
admin.site.register(Reaction)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(SavedPost)
