# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-05 14:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_mailinglistemail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='affiliation',
        ),
        migrations.AddField(
            model_name='myuser',
            name='role',
            field=models.IntegerField(default=8),
        ),
        migrations.AddField(
            model_name='myuser',
            name='role_other',
            field=models.TextField(blank=True),
        ),
    ]