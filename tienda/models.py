from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    correo = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} <{self.correo}>"


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    ESTADOS = [
        ("CREADO", "Creado"),
        ("PAGADO", "Pagado"),
        ("ENVIADO", "Enviado"),
        ("CERRADO", "Cerrado"),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="pedidos"
    )

    # 🔥 IMPORTANTE: usamos modelo intermedio
    productos = models.ManyToManyField(
        Producto,
        through='PedidoItem',
        related_name="pedidos"
    )

    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default="CREADO"
    )

    fecha = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre} ({self.estado})"


class PedidoItem(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="items"
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )

    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        # ❗ Evita duplicar el mismo producto en un pedido
        unique_together = ("pedido", "producto")

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"