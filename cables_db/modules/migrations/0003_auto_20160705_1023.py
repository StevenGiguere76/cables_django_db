# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-05 17:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0002_auto_20160701_1606'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Test',
            new_name='TestResult',
        ),
    ]