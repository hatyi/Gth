# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-02 15:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20161002_1609'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reportinputmodel',
            old_name='type',
            new_name='input_type',
        ),
    ]
