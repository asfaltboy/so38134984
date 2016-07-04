from __future__ import unicode_literals

from django.db import models


class MyTweet(models.Model):
    image = models.ImageField()
