from django.contrib import admin

# Register your models here.
from .models import CableModule
from .models import TestResult
from .models import Platform

admin.site.register(Platform)
admin.site.register(CableModule)
admin.site.register(TestResult)
