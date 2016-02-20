# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


class Subscriber(models.Model):
    uuid = models.CharField(max_length=100)

    def __str__(self):
        return self.uuid

    class Meta:
        ordering = ('pk',)


class Channel(models.Model):
    name = models.CharField(max_length=100)
    subscriber = models.ManyToManyField(Subscriber, blank=True)
    screen_name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    photo_url = models.CharField(max_length=300)
    url = models.CharField(max_length=300)
    twitter_since_id = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class News(models.Model):
    channel = models.ForeignKey(Channel, blank=True, null=True)
    url = models.CharField(max_length=2083)
    url_title = models.CharField(max_length=500, null=True, blank=True)
    url_image = models.CharField(max_length=300, null=True, blank=True)
    url_description = models.CharField(max_length=300, null=True, blank=True)
    twitter_id = models.CharField(max_length=30)
    twitter_text = models.CharField(max_length=1200)
    twitter_favorite_count = models.IntegerField(null=True, blank=True)
    twitter_retweet_count = models.IntegerField(null=True, blank=True)
    twitter_date_posted = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.twitter_id

    def __unicode__(self):
        return u'%s' % self.url_title

    class Meta:
        ordering = ('-twitter_date_posted',)
        verbose_name_plural = 'News'

