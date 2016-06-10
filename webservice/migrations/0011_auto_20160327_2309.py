# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-27 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0010_auto_20160325_2203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ('name',), 'verbose_name_plural': 'Countries'},
        ),
        migrations.AddField(
            model_name='channel',
            name='company',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channel',
            name='tag_line',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='channel',
            name='category',
        ),
        migrations.AddField(
            model_name='channel',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='category', to='webservice.Category'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='description',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='channel',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]