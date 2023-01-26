from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import VendingMachine, Snacks, Stock
from .forms import CreateVendingMachine, CreateSnack
from django.template.defaulttags import register
from django.urls import reverse


# Allows Jinja to do loops over ranges
@register.filter
def get_range(value):
    return range(value)


# multiple functions utilize snacks
snacks = Snacks.objects.all()


# =================================View Pages ================================

def vending_machine(response, loc):
    if VendingMachine.objects.filter(location=loc).count() == 0:
        return render(response, "vending/pageNotFound.html", {})
    vm = VendingMachine.objects.get(location=loc)
    stock = Stock.objects.filter(vendingMachine=vm)
    snacks = Snacks.objects.all()

    if response.method == "GET":
        return render(response, "vending/vendingMachine.html", {"vm": vm, "stock": stock, "snacks": snacks})

    return render(response, "vending/vendingMachine.html", {"vm": vm, "stock": stock, "snacks": snacks})


def home(response):
    all_vm = VendingMachine.objects.all()
    return render(response, "vending/home.html", {"allVM": all_vm, "snacks": snacks})


def stock(response):
    if response.method == "GET":
        stock = Snacks.objects.all()
        return render(response, "vending/stock.html", {"snacks": stock})
    return render(response, "vending/stock.html", {"snacks": snacks})


# ==================================Create apis=============================

def create_vm(response):
    if response.method == "POST":
        form = CreateVendingMachine(response.POST)
        if form.is_valid():
            loc = form.cleaned_data["location"]
            if VendingMachine.objects.filter(location=loc).count() == 0:
                new_vm = VendingMachine(location=loc)
                new_vm.save()
        return HttpResponseRedirect("/%s" % new_vm.location)
    else:
        form = CreateVendingMachine()
    return render(response, "vending/createVM.html", {"form": form})


# creates snacks in stock page
def create_snack(response):
    if response.method == "POST":
        name = response.POST.get("snackName")
        if snacks.filter(name=name).count() != 0:
            return render(response, "vending/stock.html", {"snacks": snacks})
        price = response.POST.get("snackPrice")
        quantity = response.POST.get("snackQty")
        new_snack = Snacks(name=name, price=price, totalQuantity=quantity, availableQuantity=quantity)
        new_snack.save()
        return stock(response)
    return stock(response)


# ==================================Delete apis===============================

# This deletes snacks from stock
def delete_stock(request, snackId):
    snack = Snacks.objects.get(id=snackId)
    snack.delete()
    return stock(request)


def delete_vm(request, vmID):
    print("deleting vm")
    vm = VendingMachine.objects.get(id=vmID)
    vm.delete()
    return HttpResponseRedirect("/")

# This deletes snacks from vending machine
def delete_snack(request, vm_id, snack_id):
    snack = Snacks.objects.get(id=snack_id)
    vm = VendingMachine.objects.get(id=vm_id)
    stock = Stock.objects.filter(vendingMachine=vm).get(snacks=snack)
    snack.availableQuantity += stock.stock
    snack.save()
    stock.delete()
    return HttpResponseRedirect("/%s" % vm.location)


# ==================================Update apis===============================

# purchase button on vending machine page
def purchase_snack(response, vmID, snackId):
    vm = VendingMachine.objects.get(id=vmID)
    snack = Snacks.objects.get(id=snackId)
    purchased_stock = Stock.objects.filter(vendingMachine=vm).get(snacks=snack)
    purchased_stock.stock -= 1
    snack.totalQuantity -= 1
    snack.availableQuantity -= 1
    purchased_stock.save()
    snack.save()
    vm.save()
    return HttpResponseRedirect("/%s" % vm.location)


# add snacks to vending machine
def add_snack_to_vm(response, vm_id):
    vm = VendingMachine.objects.get(id=vm_id)
    snack_name = response.POST.get("snackName")
    if snacks.filter(name=snack_name).count() != 0:
        snack = snacks.get(name=snack_name)
        qty = response.POST.get("snackQty")
        print(qty)
        if int(snack.availableQuantity) >= int(qty):
            new_stock = Stock(vendingMachine=vm, snacks=snack, stock=qty)
            snack.availableQuantity -= int(qty)
            new_stock.save()
            snack.save()
            vm.save()
            return vending_machine(response, vm.location)
    return vending_machine(response, vm.location)


# edit stock on vending machine page
def edit_stock_vm(response, vm_id):
    vm = VendingMachine.objects.get(id=vm_id)
    snack_name = response.POST.get("snackName")
    stock = Stock.objects.filter(vendingMachine=vm)
    if snacks.filter(name=snack_name).count() != 0 and stock.filter(snacks=snacks.get(name=snack_name)).count() != 0:
        snack = snacks.get(name=snack_name)
        qty = response.POST.get("snackQty")
        if int(snack.availableQuantity) >= int(qty):
            snack.availableQuantity = int(snack.availableQuantity) - int(qty)
            changed_stock = stock.get(snacks=snack)
            changed_stock.stock += int(qty)
            snack.save()
            changed_stock.save()
            vm.save()
            return vending_machine(response, vm.location)
    return vending_machine(response, vm.location)




# editing stock on stock page
def edit_stock(response):
    if response.method == "POST":
        snack_name = response.POST.get("snackName")
        snack_price = response.POST.get("snackPrice")
        snack_quantity = response.POST.get("editStock")
        if snacks.filter(name=snack_name).count() != 0:
            snack = snacks.get(name=snack_name)
            if snack_price != "":
                snack.price = snack_price
            if snack_quantity != "":
                snack.totalQuantity = int(snack.totalQuantity) + int(snack_quantity)
                snack.availableQuantity = int(snack.availableQuantity) + int(snack_quantity)
            snack.save()
            # return stock(response)
            return render(response, "vending/stock.html", {"snacks": snacks})
    return stock(response)
