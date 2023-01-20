from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"), #calls index by default in views.py
    path("", views.home, name="home"),
    path("<str:loc>", views.index, name="index"),
    path("createVM/", views.createVM, name="create"),
    path("createSnack/", views.createSnack, name="createSnack"),
    path("stock/", views.stock, name="stock"),
    path("deleteSnack/<int:snackId>", views.deleteSnack, name="deleteSnack"),
    path("deleteVM/<int:vmID>", views.deleteVM, name="deleteVM"),
    path("purchaseSnack/<int:vmID>/<int:snackId>/", views.purchaseSnack, name="purchaseSnack"),

]
