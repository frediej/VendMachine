from django.contrib import admin
from .models import VendingMachine, Snacks, Stock

# Register your models here.
admin.site.register(VendingMachine)
admin.site.register(Snacks)
admin.site.register(Stock)
