# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-15 05:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0002_auto_20160309_1734'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscriber',
            old_name='uuid',
            new_name='IDFA',
        ),
        migrations.AlterField(
            model_name='channel',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='webservice.Category'),
            preserve_default=False,
        ),
    ]