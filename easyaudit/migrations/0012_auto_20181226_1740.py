# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-10-18 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easyaudit', '0011_auto_20181018_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='crudevent',
            name='browser',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='crudevent',
            name='operating_system',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='loginevent',
            name='browser',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='loginevent',
            name='operating_system',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='requestevent',
            name='browser',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='requestevent',
            name='operating_system',
            field=models.CharField(max_length=100, null=True),
        ),
    ]