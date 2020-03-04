from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import redirect
import datetime

# Create your models here.
class Topic(models.Model):
    topic_text = models.CharField(max_length=200)

    def __str__(self):
        return self.topic_text
		
    class Meta:
        ordering = ['topic_text']

class Lang_tag(models.Model):
    lang_tag_text = models.CharField(max_length=200)

    def __str__(self):
        return self.lang_tag_text

class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    language = models.ForeignKey(Lang_tag, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    upvote = models.IntegerField(default=0, blank=True, null=True)
    downvote = models.IntegerField(default=0, blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=500, null=True, blank=True)
    img_url = models.CharField(max_length=500, null=True, blank=True)
    video_url = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('index')

    def was_published_recently(self):
        return self.date_posted >= timezone.now() - datetime.timedelta(days=5)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()
    comment_upvote = models.IntegerField(default=0)
    comment_downvote = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_text

    def get_absolute_url(self):
        return ('/post/%s'  %self.post.id)