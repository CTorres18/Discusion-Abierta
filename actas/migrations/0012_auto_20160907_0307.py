# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-07 06:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actas', '0011_auto_20160906_2346'),
    ]

    operations = [
        migrations.AddField(
            model_name='encuentro',
            name='complemento',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='encuentro',
            name='hash_search',
            field=models.UUIDField(default=b'6436290074c111e69c4240e230d28fea'),
        ),
    ]
