# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-09 02:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0016_auto_20171209_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='content_img'),
        ),
    ]
