# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-08 01:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_favorite'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='recipe',
            new_name='content',
        ),
    ]
