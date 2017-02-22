# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-24 12:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appoint', '0002_staffuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffNew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=25, unique=True)),
                ('username', models.CharField(max_length=40, unique=True)),
                ('user_id', models.CharField(max_length=40, unique=True)),
                ('bank_id', models.CharField(max_length=40)),
                ('counter', models.CharField(max_length=5)),
                ('password', models.CharField(max_length=40)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'appoint_staffnew',
            },
        ),
    ]
