from django.urls import path

from . import views

urlpatterns = [
    # path("", views.index, name="index"), #calls index by default in views.py
    path("", views.home, name="home"),
    path("<str:loc>", views.vending_machine, name="index"),
    path("createVM/", views.create_vm, name="create"),
    path("create_snack/", views.create_snack, name="createSnack"),
    path("stock/", views.stock, name="stock"),
    path("deleteStock/<int:snack_id>", views.delete_stock, name="deleteSnack"),
    path("deleteVM/<int:vm_id>", views.delete_vm, name="deleteVM"),
    path("purchaseSnack/<int:vm_id>/<int:snack_id>/", views.purchase_snack, name="purchaseSnack"),
    path("deleteSnack/{{ vm.id }}/{{ item.snacks.id }}", views.delete_snack, name="deleteSnack"),
    path("edit_stock/", views.edit_stock, name="editStock"),
    path("add_snack_to_vm/<int:vm_id>", views.add_snack_to_vm, name="addSnackToVM"),
    path("edit_stock_vm/<int:vm_id>", views.edit_stock_vm, name="editStockVM"),
]
