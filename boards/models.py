from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.html import mark_safe
from markdown import markdown

# 在翻译这篇文章的时候，使用的是python 3.6.4， Django 2.0.2
# ForeignKey中有一个on_delete参数

class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, models.CASCADE, related_name='topics')
    starter = models.ForeignKey(User, models.CASCADE, related_name='topics')
    views = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.subject

class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, models.CASCADE, related_name='posts')
    updated_by = models.ForeignKey(User, models.CASCADE, null=True, related_name='+')
    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)
    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
