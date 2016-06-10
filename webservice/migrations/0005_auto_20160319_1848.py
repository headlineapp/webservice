# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-19 11:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0004_newshistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='newshistory',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 3, 19, 11, 48, 19, 46207, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='newshistory',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 3, 19, 11, 48, 25, 237012, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
