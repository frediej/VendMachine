from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import VendingMachine, Snacks, Stock
from .forms import CreateVendingMachine, CreateSnack

snacks = Snacks.objects.all()

# Index is the main page for each vending machine
def index(response, loc):
    vm = VendingMachine.objects.get(location=loc)
    stock = Stock.objects.filter(vendingMachine=vm)

    # if adding a new snack for the vending machine
    if response.method == "POST":
        if response.POST.get("newSnack"):
            name = response.POST.get("name")
            price = response.POST.get("price")
            quantity = response.POST.get("quantity")
            if name == "" or price == "" or quantity == "":
                print("Inputs must be filled")
            if price.isdigit() == False or quantity.isdigit() == False:
                print("Price and quantity must be positive integers")
            if int(price) > 0 and int(quantity) > 0 and vm.snacks_set.filter(name=name).count() == 0:
                new_snack = Snacks(vending_machine=vm, name=name, price=price, quantity=quantity)
                new_snack.save()
        # if editing Vending Machine's balance
        if response.POST.get("editBalance"):
            balance = response.POST.get("balance")
            if balance != "" and int(balance) >= 0:
                vm.balance = balance
                vm.save()
                print("balance updated")
                # return JsonResponse({"balance": balance})
        elif response.POST.get("editSnack"):
            name = response.POST.get("snackName")
            print(name)
            price = response.POST.get("snackPrice")
            quantity = response.POST.get("snackQuantity")
            if name == "" or price == "" or quantity == "":
                print("Inputs must be filled")
            if price.isdigit() == False or quantity.isdigit() == False:
                print("Price and quantity must be positive integers")
            if int(price) >= 0 and int(quantity) >= 0:
                snack = vm.snacks_set.get(name=name)
                snack.price = price
                snack.quantity = quantity
                snack.save()
                # return JsonResponse({"name": name, "price": price, "quantity": quantity})
    return render(response, "vending/vendingMachine.html", {"vm": vm, "stock": stock, "snacks": snacks})


def home(response):
    allVM = VendingMachine.objects.all()
    return render(response, "vending/home.html", {"allVM": allVM})
    # return render(response, "vending/home.html", {})


def create(response):
    if response.method == "POST":
        form = CreateVendingMachine(response.POST)
        if form.is_valid():
            loc = form.cleaned_data["location"]
            b = form.cleaned_data["balance"]
            new_vm = VendingMachine(location=loc, balance=b)
            new_vm.save()
        return HttpResponseRedirect("/%s" % new_vm.location)
    else:
        form = CreateVendingMachine()
    return render(response, "vending/create.html", {"form": form})

def transaction(response):
    # if response.method == "POST":
    #     loc = response.POST.get("location")
    #     vm = VendingMachine.objects.get(location=loc)
    #     snack = response.POST.get("snack")
    #     snack = vm.snacks_set.get(name=snack)
    #     if snack.quantity > 0 and vm.balance >= snack.price:
    #         snack.quantity -= 1
    #         snack.save()
    #         vm.balance -= snack.price
    #         vm.save()
    # return HttpResponseRedirect("/%s" % loc)
    vm = VendingMachine.objects.all()
    snacks = Snacks.objects.all()
    return render(response, "vending/transaction.html", {"snacks": snacks, "vm": vm})
