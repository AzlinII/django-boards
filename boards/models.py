from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.db.models import Count


# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by("-created_at").first()

    def get_topics_with_replies(self):
        return self.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete="cascade")
    starter = models.ForeignKey(User, related_name='topics', on_delete="cascade")
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete="cascade")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete="cascade")
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete="casacade")

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

