# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-08 03:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_remove_content_fav_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='text',
            field=models.CharField(max_length=1000),
        ),
    ]