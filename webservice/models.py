from __future__ import unicode_literals

from django.db import models

class Channel(models.Model):
    name = models.CharField(max_length=100)
    screen_name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    photo_url = models.CharField(max_length=300)
    url = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class News(models.Model):
    source = models.ForeignKey(Channel)
    text = models.CharField(max_length=300)
    date_created = models.DateTimeField(auto_now=False)
    url = models.CharField(max_length=300)
    url_image = models.CharField(max_length=300)
    url_description = models.CharField(max_length=300)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('date_created',)
        verbose_name_plural = 'News'


class Subscriber(models.Model):
    uuid = models.CharField(max_length=100)
    subscribes = models.ManyToManyField(Channel)
    bookmarks = models.ManyToManyField(News, related_name="bookmarks")
    reading_list = models.ManyToManyField(News, related_name="reading_list")

    def __str__(self):
        return self.uuid

    class Meta:
        ordering = ('uuid',)

