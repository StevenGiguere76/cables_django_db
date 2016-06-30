from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Platform(models.Model):
    platform_name = models.CharField('Platform Name', max_length=64)

class CableModule(models.Model):
    printed_label = models.CharField('Printed Label', max_length=64)
    vendor_name = models.CharField('Vendor Name', max_length=64)
    pin_number = models.CharField('Vendor Pin Number', max_length=64)
    serial_number = models.CharField('Vendor Serial Number', max_length=64)
    vendor_oui = models.CharField('Vendor OUI', max_length=64)
    manufactorer = models.CharField('Manufactorer', max_length=64)
    form_factor = models.CharField('Form Factor', max_length=64)
    speed = models.CharField('Default Speed', max_length=64)
    mod_type = models.CharField('Module Type', max_length=64)
    length = models.SmallIntegerField('Length')

class Test(models.Model):
    date_tested = models.DateField('Date Tested', auto_now=True)
    qsa_used = models.BooleanField('QSA Used?')
    speed = models.CharField('Speed Tested', max_length=64)
    bug_id = models.URLField('Bug-ID')
    test_passed = models.BooleanField('Pass?')
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    module = models.ForeignKey(CableModule, on_delete=models.CASCADE)
