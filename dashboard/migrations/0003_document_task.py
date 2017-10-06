# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 20:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='task',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Task'),
            preserve_default=False,
        ),
    ]
