from django.db import models

# Create your models here.

class VendingMachine(models.Model):
    # name = models.CharField(max_length=100)
    # price = models.IntegerField()
    # quantity = models.IntegerField()
    # def __str__(self):
    #     return self.name
    location = models.CharField(max_length=200)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.location

class Snacks(models.Model):
    vending_machine = models.ForeignKey(VendingMachine, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.name
