from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Comment

# admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Post, MarkdownxModelAdmin)
