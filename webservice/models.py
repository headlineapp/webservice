# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Subscriber(models.Model):
    uuid = models.CharField(max_length=100)
    country = models.ManyToManyField(Country, blank=True)

    def __str__(self):
        return self.uuid

    class Meta:
        ordering = ('pk',)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Channel(models.Model):
    name = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)
    subscriber = models.ManyToManyField(Subscriber, blank=True)
    description = models.CharField(max_length=300)
    photo_url = models.CharField(max_length=300)
    url = models.CharField(max_length=300)
    twitter_screen_name = models.CharField(max_length=100)
    twitter_since_id = models.CharField(max_length=30, null=True, blank=True)
    twitter_last_date = models.DateTimeField(null=True, blank=True)
    country = models.ManyToManyField(Country, blank=True)
    latest_news = models.ManyToManyField('News', blank=True, related_name='latest_news')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class News(models.Model):
    channel = models.ForeignKey(Channel, blank=True, null=True)
    url = models.CharField(max_length=2083)
    url_title = models.CharField(max_length=500, null=True, blank=True)
    url_image = models.CharField(max_length=300, null=True, blank=True)
    url_description = models.CharField(max_length=2000, null=True, blank=True)
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

