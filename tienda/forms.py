from django import forms
from django.forms import inlineformset_factory
from .models import Producto, Cliente, Pedido, PedidoItem


# 🔹 FORM CLIENTE
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "correo", "activo"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "placeholder": "Nombre completo",
                "class": "form-control"
            }),
            "correo": forms.EmailInput(attrs={
                "placeholder": "correo@ejemplo.com",
                "class": "form-control"
            }),
        }


# 🔹 FORM PRODUCTO
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "precio", "imagen"]

        widgets = {
            "nombre": forms.TextInput(attrs={
                "placeholder": "Nombre del producto",
                "class": "form-control"
            }),
            "descripcion": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Descripción breve",
                "class": "form-control"
            }),
            "precio": forms.NumberInput(attrs={
                "step": "0.01",
                "min": "0",
                "class": "form-control"
            }),
            "imagen": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }

    def clean_precio(self):
        precio = self.cleaned_data.get("precio")
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor que 0")
        return precio


# 🔹 FORM PEDIDO SIMPLE
class PedidoSimpleForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["cliente", "estado"]
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-control"}),
            "estado": forms.Select(attrs={"class": "form-control"}),
        }


# 🔹 FORM ITEM (PRODUCTO + CANTIDAD)
class PedidoItemForm(forms.ModelForm):
    class Meta:
        model = PedidoItem
        fields = ["producto", "cantidad"]
        widgets = {
            "producto": forms.Select(attrs={"class": "form-control"}),
            "cantidad": forms.NumberInput(attrs={
                "min": 1,
                "class": "form-control"
            }),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get("cantidad")
        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor a 0")
        return cantidad


# 🔥 FORMSET (VARIOS PRODUCTOS EN UN PEDIDO)
PedidoItemFormSet = inlineformset_factory(
    Pedido,
    PedidoItem,
    form=PedidoItemForm,
    extra=1,
    can_delete=True
)