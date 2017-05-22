from django.db import models
from django.utils import timezone

from taggit.managers import TaggableManager
from taggit.models import Tag

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    # text = models.TextField()
    text = MarkdownxField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    tags = TaggableManager()

    @property
    def markdown_to_html(self):
        return markdownify(self.text)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text