from django.db import models

# Create your models here.


class VendingMachine(models.Model):
    location = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.location


class Snacks(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    totalQuantity = models.IntegerField()
    availableQuantity = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name


class Stock(models.Model):
    vendingMachine = models.ForeignKey(VendingMachine, on_delete=models.CASCADE)
    snacks = models.ForeignKey(Snacks, on_delete=models.CASCADE)
    stock = models.IntegerField()

    def __str__(self) -> str:
        return self.snacks.name + " " + str(self.stock)
