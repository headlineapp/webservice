# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-19 13:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0007_auto_20160319_1952'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bookmarks',
            new_name='Bookmark',
        ),
    ]
