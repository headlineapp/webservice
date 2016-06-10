# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-19 12:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0006_newshistory_number_of_visit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmarks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webservice.News')),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webservice.Subscriber')),
            ],
        ),
        migrations.RenameModel(
            old_name='NewsHistory',
            new_name='History',
        ),
    ]
