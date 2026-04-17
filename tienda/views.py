from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.db.models import Sum, F, Value, DecimalField, ExpressionWrapper
from django.db.models.functions import Coalesce

from .models import Producto, Pedido, Cliente
from .forms import ProductoForm, ClienteForm, PedidoSimpleForm, PedidoItemFormSet


# 🏠 HOME
def home(request):
    return render(request, "tienda/home.html")


# 📦 PRODUCTOS
def lista_productos(request):
    productos = Producto.objects.all().order_by("nombre")
    return render(request, "tienda/lista_productos.html", {
        "productos": productos
    })


def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, "tienda/detalle_producto.html", {
        "producto": producto
    })


def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("tienda:lista_productos")
    else:
        form = ProductoForm()

    return render(request, "tienda/crear_producto.html", {
        "form": form
    })


def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("tienda:detalle_producto", pk=producto.pk)
    else:
        form = ProductoForm(instance=producto)

    return render(request, "tienda/editar_producto.html", {
        "form": form,
        "producto": producto
    })


def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        producto.delete()
        return redirect("tienda:lista_productos")

    return render(request, "tienda/eliminar_producto.html", {
        "producto": producto
    })


# 👤 CLIENTES
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by("nombre")
    return render(request, "tienda/lista_clientes.html", {
        "clientes": clientes
    })


def crear_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tienda:lista_clientes")
    else:
        form = ClienteForm()

    return render(request, "tienda/crear_cliente.html", {
        "form": form
    })


# 📦 CREAR PEDIDO (CON ITEMS)
@transaction.atomic
def crear_pedido_items(request):
    if request.method == "POST":
        pedido_form = PedidoSimpleForm(request.POST)

        if pedido_form.is_valid():
            pedido = pedido_form.save()

            formset = PedidoItemFormSet(request.POST, instance=pedido)

            if formset.is_valid():
                formset.save()
                return redirect("tienda:detalle_pedido", pk=pedido.pk)

    else:
        pedido_form = PedidoSimpleForm()
        formset = PedidoItemFormSet()

    return render(request, "tienda/crear_pedido_items.html", {
        "pedido_form": pedido_form,
        "formset": formset
    })


# ✏️ EDITAR PEDIDO
@transaction.atomic
def editar_pedido_items(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == "POST":
        pedido_form = PedidoSimpleForm(request.POST, instance=pedido)

        if pedido_form.is_valid():
            pedido = pedido_form.save()

            formset = PedidoItemFormSet(request.POST, instance=pedido)

            if formset.is_valid():
                formset.save()
                return redirect("tienda:detalle_pedido", pk=pedido.pk)

    else:
        pedido_form = PedidoSimpleForm(instance=pedido)
        formset = PedidoItemFormSet(instance=pedido)

    return render(request, "tienda/editar_pedido.html", {
        "pedido_form": pedido_form,
        "formset": formset,
        "pedido": pedido
    })


# 📦 LISTA PEDIDOS (CON TOTALES)
def lista_pedidos(request):
    pedidos = Pedido.objects.annotate(
        total_productos=Coalesce(Sum("items__cantidad"), Value(0)),
        total_precio=Coalesce(
            Sum(
                ExpressionWrapper(
                    F("items__cantidad") * F("items__producto__precio"),
                    output_field=DecimalField(max_digits=10, decimal_places=2)
                )
            ),
            Value(0),
            output_field=DecimalField()
        )
    ).order_by("-fecha")

    return render(request, "tienda/lista_pedidos.html", {
        "pedidos": pedidos
    })


# 🔍 DETALLE PEDIDO
def detalle_pedido(request, pk):
    pedido = get_object_or_404(
        Pedido.objects.select_related("cliente")
        .prefetch_related("items__producto"),
        pk=pk
    )

    items = pedido.items.all()

    total_unidades = sum(item.cantidad for item in items)
    total_pedido = sum(item.cantidad * item.producto.precio for item in items)

    for item in items:
        item.line_total = item.cantidad * item.producto.precio

    return render(request, "tienda/detalle_pedido.html", {
        "pedido": pedido,
        "items": items,
        "total_unidades": total_unidades,
        "total_pedido": total_pedido
    })


# 🗑 ELIMINAR PEDIDO
def eliminar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == "POST":
        pedido.delete()
        return redirect("tienda:lista_pedidos")

    return render(request, "tienda/eliminar_pedido.html", {
        "pedido": pedido
    })