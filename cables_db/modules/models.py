from __future__ import unicode_literals

from django.db import models
from datetime import date

# Create your models here.

class Platform(models.Model):
    platform_name = models.CharField('Platform Name', max_length=64)

    def __str__(self):
        return self.platform_name

class CableModule(models.Model):
    printed_label = models.CharField('Printed Label', max_length=64)
    vendor_name = models.CharField('Vendor Name', max_length=64)
    pin_number = models.CharField('Vendor Pin Number', max_length=64)
    serial_number = models.CharField('Vendor Serial Number', max_length=64)
    vendor_oui = models.CharField('Vendor OUI', max_length=64)
    vendor_rev = models.CharField('Vendor Rev', max_length=64)
    form_factor = models.CharField('Form Factor', max_length=64)
    speed = models.CharField('Default Speed', max_length=64)
    mod_type = models.CharField('Module Type', max_length=64)
    length = models.SmallIntegerField('Length')

    def __str__(self):
        build_string = '[Vendor Name: {0}, Vendor_SN: {1}, Vendor_PN: {2}]'.format(self.vendor_name, self.serial_number, self.pin_number)

        return build_string

class TestResult(models.Model):
    date_tested = models.DateField('Date Tested', auto_now_add=True)
    qsa_used = models.BooleanField('QSA Used?')
    speed = models.CharField('Speed Tested', max_length=64)
    bug_id = models.URLField('Bug-ID', null=True)
    test_passed = models.BooleanField('Pass?')
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    module = models.ForeignKey(CableModule, on_delete=models.CASCADE)

    def __str__(self):
        build_string = 'Platform: {0}\n' \
        'Module: {1}\n' \
        'Speed: {2}\n' \
        'QSA_Used: {3}\n' \
        'Test Passed: {4}\n' \
        'Date Tested: {5}\n' \
        'Bug ID: {6}\n'.format(self.platform, self.module, self.speed, self.qsa_used, self.test_passed, self.date_tested, self.bug_id)

        return build_string
