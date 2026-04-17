from django.urls import path
from . import views

app_name = "tienda"

urlpatterns = [
    path("", views.home, name="home"),

    # 📦 Productos
    path("productos/", views.lista_productos, name="lista_productos"),
    path("productos/<int:pk>/", views.detalle_producto, name="detalle_producto"),
    path("productos/nuevo/", views.crear_producto, name="crear_producto"),
    path("productos/<int:pk>/editar/", views.editar_producto, name="editar_producto"),
    path("productos/<int:pk>/eliminar/", views.eliminar_producto, name="eliminar_producto"),

    # 👤 Clientes
    path("clientes/", views.lista_clientes, name="lista_clientes"),
    path("clientes/crear/", views.crear_cliente, name="crear_cliente"),

    # 📦 Pedidos
    path("pedidos/", views.lista_pedidos, name="lista_pedidos"),
    path("pedidos/nuevo/", views.crear_pedido_items, name="crear_pedido"),
    path("pedidos/<int:pk>/", views.detalle_pedido, name="detalle_pedido"),
    path("pedidos/<int:pk>/editar/", views.editar_pedido_items, name="editar_pedido"),
    path("pedidos/<int:pk>/eliminar/", views.eliminar_pedido, name="eliminar_pedido"),
]