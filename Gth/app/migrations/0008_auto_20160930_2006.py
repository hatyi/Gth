# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-30 18:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20160930_1910'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportInputGroupModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('page_order', models.SmallIntegerField(default=1)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='app.Page')),
            ],
        ),
        migrations.AddField(
            model_name='reportinputmodel',
            name='group_order',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='reportinputmodel',
            name='group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inputs', to='app.ReportInputGroupModel'),
        ),
    ]
