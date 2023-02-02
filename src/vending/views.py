from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.defaulttags import register

from .forms import CreateVendingMachine
from .models import Snacks, Stock, VendingMachine


# Allows Jinja to do loops over ranges
@register.filter
def get_range(value: any) -> any:
    return range(value)


# multiple functions utilize snacks
snacks = Snacks.objects.all()
stock_html = "vending/stock.html"

# =================================View Pages ================================


def vending_machine(request: HttpRequest, loc: str) -> HttpResponse:
    if VendingMachine.objects.filter(location=loc).count() == 0:
        return render(request, "vending/pageNotFound.html", {})
    vm = VendingMachine.objects.get(location=loc)
    stock = Stock.objects.filter(vendingMachine=vm)
    snacks = Snacks.objects.all()

    if request.method == "GET":
        return render(request, "vending/vendingMachine.html", {"vm": vm, "stock": stock, "snacks": snacks})

    return render(request, "vending/vendingMachine.html", {"vm": vm, "stock": stock, "snacks": snacks})


def home(request: HttpRequest) -> HttpResponse:
    all_vm = VendingMachine.objects.all()
    return render(request, stock_html, {"allVM": all_vm, "snacks": snacks})


def stock(request: HttpRequest) -> HttpResponse:
    return render(request, "vending/stock.html", {"snacks": snacks})


# ==================================Create apis=============================


def create_vm(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CreateVendingMachine(request.POST)
        if form.is_valid():
            loc = form.cleaned_data["location"]
            if VendingMachine.objects.filter(location=loc).count() == 0:
                new_vm = VendingMachine(location=loc)
                new_vm.save()
        return HttpResponseRedirect("/%s" % new_vm.location)
    else:
        form = CreateVendingMachine()
    return render(request, "vending/createVM.html", {"form": form})


# creates snacks in stock page
def create_snack(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        name = request.POST.get("snackName")
        if snacks.filter(name=name).count() != 0:
            return render(request, stock_html, {"snacks": snacks})
        price = request.POST.get("snackPrice")
        quantity = request.POST.get("snackQty")
        new_snack = Snacks(name=name, price=price, totalQuantity=quantity, availableQuantity=quantity)
        new_snack.save()
        return stock(request)
    return stock(request)


# ==================================Delete apis===============================

# This deletes snacks from stock
def delete_stock(request: HttpRequest, snack_id: int) -> HttpResponse:
    snack = Snacks.objects.get(id=snack_id)
    snack.delete()
    return stock(request)


def delete_vm(vm_id: int) -> HttpResponseRedirect:
    print("deleting vm")
    vm = VendingMachine.objects.get(id=vm_id)
    vm.delete()
    return HttpResponseRedirect("/")


# This deletes snacks from vending machine
def delete_snack(vm_id: int, snack_id: int) -> HttpResponseRedirect:
    snack = Snacks.objects.get(id=snack_id)
    vm = VendingMachine.objects.get(id=vm_id)
    stock = Stock.objects.filter(vendingMachine=vm).get(snacks=snack)
    snack.availableQuantity += stock.stock
    snack.save()
    stock.delete()
    return HttpResponseRedirect("/%s" % vm.location)


# ==================================Update apis===============================

# purchase button on vending machine page
def purchase_snack(vm_id: int, snack_id: int) -> HttpResponseRedirect:
    vm = VendingMachine.objects.get(id=vm_id)
    snack = Snacks.objects.get(id=snack_id)
    purchased_stock = Stock.objects.filter(vendingMachine=vm).get(snacks=snack)
    purchased_stock.stock -= 1
    snack.totalQuantity -= 1
    snack.availableQuantity -= 1
    purchased_stock.save()
    snack.save()
    vm.save()
    return HttpResponseRedirect("/%s" % vm.location)


# add snacks to vending machine
def add_snack_to_vm(request: HttpRequest, vm_id: int) -> HttpResponse:
    vm = VendingMachine.objects.get(id=vm_id)
    snack_name = request.POST.get("snackName")
    if snacks.filter(name=snack_name).count() != 0:
        snack = snacks.get(name=snack_name)
        qty = request.POST.get("snackQty")
        print(qty)
        if int(snack.availableQuantity) >= int(qty):
            new_stock = Stock(vendingMachine=vm, snacks=snack, stock=qty)
            snack.availableQuantity -= int(qty)
            new_stock.save()
            snack.save()
            vm.save()
            return vending_machine(request, vm.location)
    return vending_machine(request, vm.location)


# edit stock on vending machine page
def edit_stock_vm(request: HttpRequest, vm_id: int) -> HttpResponse:
    vm = VendingMachine.objects.get(id=vm_id)
    snack_name = request.POST.get("snackName")
    stock = Stock.objects.filter(vendingMachine=vm)
    if snacks.filter(name=snack_name).count() != 0 and stock.filter(snacks=snacks.get(name=snack_name)).count() != 0:
        snack = snacks.get(name=snack_name)
        qty = request.POST.get("snackQty")
        if int(snack.availableQuantity) >= int(qty):
            snack.availableQuantity = int(snack.availableQuantity) - int(qty)
            changed_stock = stock.get(snacks=snack)
            changed_stock.stock += int(qty)
            snack.save()
            changed_stock.save()
            vm.save()
            return vending_machine(request, vm.location)
    return vending_machine(request, vm.location)


# editing stock on stock page
def edit_stock(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        snack_name = request.POST.get("snackName")
        snack_price = request.POST.get("snackPrice")
        snack_quantity = request.POST.get("editStock")
        if snacks.filter(name=snack_name).count() != 0:
            snack = snacks.get(name=snack_name)
            if snack_price != "":
                snack.price = snack_price
            if snack_quantity != "":
                snack.totalQuantity = int(snack.totalQuantity) + int(snack_quantity)
                snack.availableQuantity = int(snack.availableQuantity) + int(snack_quantity)
            snack.save()
            return render(request, stock_html, {"snacks": snacks})
    return stock(request)
