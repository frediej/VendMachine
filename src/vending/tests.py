import os

import django
from django.test import TestCase

from .models import Snacks, Stock, VendingMachine

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw1.settings")
django.setup()


# Create your tests here.

LOCATION = "test"


class VMTestCase(TestCase):
    def setUp(self):
        vm = VendingMachine.objects.create(location=LOCATION)
        vm.save()

    def test_vm_creation(self):
        vm = VendingMachine.objects.get(location=LOCATION)
        self.assertTrue(vm.location == LOCATION)


SNACK_NAME = "test"
SNACK_PRICE = 1
SNACK_TOTAL_QUANTITY = 1
SNACK_AVAILABLE_QUANTITY = 1


class SnackTestCase(TestCase):
    def setUp(self):
        snackie = Snacks.objects.create(
            name=SNACK_NAME,
            price=SNACK_PRICE,
            totalQuantity=SNACK_TOTAL_QUANTITY,
            availableQuantity=SNACK_AVAILABLE_QUANTITY,
        )
        snackie.save()

    #
    def test_snack_creation(self):
        snackie = Snacks.objects.get(name=SNACK_NAME)
        self.assertTrue(snackie.name == SNACK_NAME)
        self.assertTrue(snackie.price == SNACK_PRICE)
        self.assertTrue(snackie.totalQuantity == SNACK_TOTAL_QUANTITY)
        self.assertTrue(snackie.availableQuantity == SNACK_AVAILABLE_QUANTITY)


STOCK = 1


class StockTestCase(TestCase):
    def setUp(self):
        vm = VendingMachine.objects.create(location=LOCATION)
        vm.save()
        snackie = Snacks.objects.create(
            name=SNACK_NAME,
            price=SNACK_PRICE,
            totalQuantity=SNACK_TOTAL_QUANTITY,
            availableQuantity=SNACK_AVAILABLE_QUANTITY,
        )
        snackie.save()
        stockie = Stock.objects.create(vendingMachine=vm, snacks=snackie, stock=STOCK)
        stockie.save()

    def test_stock_creation(self):
        stockie = Stock.objects.get(snacks__name=SNACK_NAME)
        self.assertTrue(stockie.stock == STOCK)
