from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.conf import settings

from django.db import models


class Story(models.Model):
    title = models.CharField(max_length=255)
    current_tweet = models.ForeignKey(
        'Tweet', related_name='current_story', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    votes = models.PositiveIntegerField(default=0)
    story = models.ForeignKey(
        Story, related_name='tweets', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}: {self.content}'
