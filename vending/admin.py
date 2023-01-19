from django.contrib import admin
from .models import VendingMachine, Snacks

# Register your models here.
admin.site.register(VendingMachine)
admin.site.register(Snacks)
