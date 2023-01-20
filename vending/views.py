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


# Index is the main page for each vending machine
def index(response, loc):
    if VendingMachine.objects.filter(location=loc).count() == 0:
        return render(response, "vending/pageNotFound.html", {})
    vm = VendingMachine.objects.get(location=loc)
    stock = Stock.objects.filter(vendingMachine=vm)
    snacks = Snacks.objects.all()

    if response.method == "GET":
        return render(response, "vending/vendingMachine.html", {"vm": vm, "stock": stock, "snacks": snacks})
    # if adding a new snack for the vending machine

    if response.method == "POST":

        # add snack to vending machine
        if response.POST.get("addSnack"):
            snackName = response.POST.get("snackName")
            qty = response.POST.get("snackQty")
            snack = Snacks.objects.get(name=snackName)
            if stock.filter(snacks=snack).count() != 0:
                changeStock = Stock.objects.get(snacks=snack)
                if int(snack.availableQuantity) >= int(qty) + int(changeStock.stock):
                    changeStock.stock = int(changeStock.stock) + int(qty)
                    snack.availableQuantity = int(snack.availableQuantity) - int(qty)
                    changeStock.save()
                    snack.save()
                    vm.save()
                    return HttpResponseRedirect("/%s" % loc)
            elif int(snack.availableQuantity) >= int(qty):
                newStock = Stock(vendingMachine=vm, snacks=snack, stock=qty)
                snack.availableQuantity = int(snack.availableQuantity) - int(qty)
                newStock.save()
                snack.save()
                vm.save()
                return render(response, "vending/vendingMachine.html", {"vm": vm, "stock": stock, "snacks": snacks})

        # Edit stock in vending machine, simply replaces the stock
        elif response.POST.get("editStock"):
            snackName = response.POST.get("snackName")
            qty = response.POST.get("snackQty")
            snack = Snacks.objects.get(name=snackName)
            changeStock = Stock.objects.get(snacks=snack)
            if int(snack.availableQuantity) >= int(qty):
                snack.availableQuantity = int(snack.availableQuantity) - int(qty) + int(changeStock.stock)
                changeStock.stock = int(qty)
                changeStock.save()
                snack.save()
                vm.save()
                return render(response, "vending/vendingMachine.html", {"vm": vm, "stock": stock, "snacks": snacks})
        else:
            return render(response, "vending/pageNotFound.html", {})
    # return render(response, "vending/vendingMachine.html", {"vm": vm, "stock": stock, "snacks": snacks})


def home(response):
    allVM = VendingMachine.objects.all()
    return render(response, "vending/home.html", {"allVM": allVM, "snacks": snacks})


# creates vending machines
def createVM(response):
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


# creates snacks
def createSnack(response):
    if response.method == "GET":
        stock = Snacks.objects.all()
        return render(response, "vending/createSnack.html", {"snacks": stock})
    if response.method == "POST":
        form = CreateSnack(response.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            price = form.cleaned_data["price"]
            quantity = form.cleaned_data["quantity"]
            if snacks.filter(name=name).count() == 0:
                new_snack = Snacks(name=name, price=price, totalQuantity=quantity, availableQuantity=quantity)
                new_snack.save()
                return HttpResponseRedirect("/")
        return HttpResponseRedirect("")
    else:
        form = CreateSnack()
    return render(response, "vending/createSnack.html", {"form": form})


def stock(response):
    if response.method == "GET":
        stock = Snacks.objects.all()
        return render(response, "vending/stock.html", {"snacks": stock})
    if response.method == "POST":
        if response.POST.get("createSnack"):
            name = response.POST.get("snackName")
            if snacks.filter(name=name).count() != 0:
                return render(response, "vending/stock.html", {"snacks": snacks})
            price = response.POST.get("snackPrice")
            quantity = response.POST.get("snackQty")
            new_snack = Snacks(name=name, price=price, totalQuantity=quantity, availableQuantity=quantity)
            new_snack.save()
            new_snacks = Snacks.objects.all()
            return render(response, "vending/stock.html", {"snacks": new_snacks})
        elif response.POST.get("editSnack"):
            name = response.POST.get("snackName")
            if snacks.filter(name=name).count() != 0:
                snack = snacks.get(name=name)
                price = response.POST.get("snackPrice")
                if price != "":
                    snack.price = price
                quantity = response.POST.get("snackQty")
                if quantity != "":
                    pass
                snack.totalQuantity = response.POST.get("snackQty")
                snack.availableQuantity = response.POST.get("snackQty")
                snack.save()
                new_snacks = Snacks.objects.all()
                return render(response, "vending/stock.html", {"snacks": new_snacks})
                snack.save()
    return render(response, "vending/stock.html", {"snacks": snacks})


#delete button on stock page
def deleteSnack(request, snackId):
    snack = Snacks.objects.get(id=snackId)
    snack.delete()
    return HttpResponseRedirect("/stock")

def deleteVM(request, vmId):
    print("deleting vm")
    vm = VendingMachine.objects.get(id=vmId)
    vm.delete()
    return HttpResponseRedirect("/")

# purchase button on vending machine page
def purchaseSnack(request, vmID, snackId):
    vm = VendingMachine.objects.get(id=vmID)
    snack = Snacks.objects.get(id=snackId)
    purchasedStock = Stock.objects.filter(vendingMachine=vm).get(snacks=snack)
    purchasedStock.stock -= 1
    snack.totalQuantity -= 1
    snack.availableQuantity -= 1
    purchasedStock.save()
    snack.save()
    return HttpResponseRedirect("/%s" % vm.location)
