from django.contrib import admin

from .models import Post, Reaction, Tag, SavedPost

admin.site.register(Post)
admin.site.register(Reaction)
admin.site.register(Tag)
admin.site.register(SavedPost)