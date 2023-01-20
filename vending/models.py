from django.db import models


# Create your models here.

class VendingMachine(models.Model):
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.location


class Snacks(models.Model):
    # vending_machine = models.ForeignKey(VendingMachine, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    totalQuantity = models.IntegerField()
    availableQuantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Stock(models.Model):
    vendingMachine = models.ForeignKey(VendingMachine, on_delete=models.CASCADE)
    snacks = models.ForeignKey(Snacks, on_delete=models.CASCADE)
    stock = models.IntegerField()

    def __str__(self):
        return self.snacks.name + " " + str(self.stock)
