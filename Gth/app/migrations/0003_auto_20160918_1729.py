# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-18 15:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20160918_1722'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reportresult',
            old_name='user',
            new_name='profile',
        ),
    ]
