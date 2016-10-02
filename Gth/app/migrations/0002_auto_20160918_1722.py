# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-18 15:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finished_editing_timestamp', models.DateTimeField()),
                ('uploaded_timestamp', models.DateTimeField()),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='report_results', to='app.Report')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='app.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='ReportResultInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_value', models.CharField(max_length=255)),
                ('date_value', models.DateTimeField()),
                ('range_value', models.FloatField()),
                ('signature_value', models.FileField(upload_to='')),
            ],
        ),
        migrations.RenameField(
            model_name='choicemodel',
            old_name='needs_comment',
            new_name='must_comment',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='profile',
        ),
        migrations.AddField(
            model_name='reportinputmodel',
            name='can_comment',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='reportinputmodel',
            name='must_comment',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reportinputmodel',
            name='page_order',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='reportinputmodel',
            name='type',
            field=models.SmallIntegerField(choices=[(0, 'Text'), (1, 'Date'), (2, 'Range'), (3, 'Choices'), (4, 'Signature')], default=0),
        ),
        migrations.AddField(
            model_name='reportresultinput',
            name='choice_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dk_3', to='app.ChoiceModel'),
        ),
        migrations.AddField(
            model_name='reportresultinput',
            name='input_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='input_results', to='app.ReportInputModel'),
        ),
        migrations.AddField(
            model_name='comment',
            name='target_input',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='app.ReportResultInput'),
        ),
    ]
