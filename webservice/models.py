# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Countries'


class Subscriber(models.Model):
    IDFA = models.CharField(max_length=100, unique=True)
    country = models.ManyToManyField(Country, blank=True)
    channel = models.ManyToManyField('Channel', blank=True)

    def __str__(self):
        return self.IDFA

    class Meta:
        ordering = ('pk',)


class Category(models.Model):
    name = models.CharField(max_length=100)
    number_of_channel = models.IntegerField(default=0)
    category_icon_url = models.CharField(max_length=300, default='')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'


class Channel(models.Model):
    name = models.CharField(max_length=100)
    tag_line = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    category = models.ManyToManyField(Category, blank=True, related_name='category')
    twitter_screen_name = models.CharField(max_length=100)
    twitter_since_id = models.CharField(max_length=30, null=True, blank=True)
    twitter_last_date = models.DateTimeField(null=True, blank=True)
    profile_image_url = models.CharField(max_length=300)
    url = models.CharField(max_length=300)
    country = models.ManyToManyField(Country, blank=True)
    latest_news = models.ManyToManyField('News', blank=True, related_name='latest_news')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class News(models.Model):
    channel = models.ForeignKey(Channel, blank=True, null=True, unique=True)
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


class History(models.Model):
    subscriber = models.ForeignKey(Subscriber)
    news = models.ForeignKey(News)
    number_of_visit = models.IntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_date',)
        verbose_name_plural = 'Histories'


class Bookmark(models.Model):
    subscriber = models.ForeignKey(Subscriber)
    news = models.ForeignKey(News)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_date',)
        verbose_name_plural = 'Bookmark'