from django.shortcuts import render, get_object_or_404
from .models import Producto
from .models import Pedido

def home(request):
    return render(request, "tienda/home.html")

def lista_productos(request):
    productos = Producto.objects.all().order_by("nombre")

    return render(request, "tienda/lista_productos.html", {"productos": productos})

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, "tienda/detalle_producto.html", {"producto": producto})

def lista_pedidos(request):
    # Traemos todos los pedidos ordenados por fecha
    pedidos = Pedido.objects.all().order_by("-fecha")  # los más recientes primero

    return render(request, "tienda/lista_pedidos.html", {
        "pedidos": pedidos
    })