from django import forms


class CreateVendingMachine(forms.Form):
    location = forms.CharField(label="Location", max_length=200)


class CreateSnack(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    price = forms.IntegerField(label="Price")
    quantity = forms.IntegerField(label="Quantity")

