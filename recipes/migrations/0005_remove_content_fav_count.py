# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-08 02:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_content_fav_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='fav_count',
        ),
    ]
