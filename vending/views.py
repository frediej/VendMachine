from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import VendingMachine, Snacks
from .forms import CreateVendingMachine, CreateSnack


# Create your views here.
def index(response, loc):
    vm = VendingMachine.objects.get(location=loc)

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
                # return JsonResponse({"name": name, "price": price, "quantity": quantity}) returning jsonresponse here wou
        elif response.POST.get("editBalance"):
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
    return render(response, "vending/vendingMachine.html", {"vm": vm})


def home(response):
    return render(response, "vending/home.html", {})


def create(response):
    if response.method == "POST":
        form = CreateVendingMachine(response.POST)
        if form.is_valid():
            loc = form.cleaned_data["location"]
            b = form.cleaned_data["balance"]
            new_vm = VendingMachine(location=loc, balance=b)
            new_vm.save()
            return JsonResponse({"location": loc, "balance": b})
        # return HttpResponseRedirect("/%s" % new_vm.location)
    else:
        form = CreateVendingMachine()
    return render(response, "vending/create.html", {"form": form})
