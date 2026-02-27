from django.urls import path
from . import views

app_name = "tienda"

urlpatterns = [
    path("", views.home, name="home"),
    path("productos/", views.lista_productos, name="lista_productos"),
    path("producto/<int:pk>/", views.detalle_producto, name="detalle_producto"),  # producto
    path("pedidos/", views.lista_pedidos, name="lista_pedidos"), #pedidos
]