# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-05 21:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0005_auto_20160705_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresult',
            name='date_tested',
            field=models.DateField(default=datetime.datetime(2016, 7, 5, 21, 20, 0, 49181, tzinfo=utc), verbose_name='Date Tested'),
        ),
    ]
