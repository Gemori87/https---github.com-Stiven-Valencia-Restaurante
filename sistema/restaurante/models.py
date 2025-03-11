from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Platillos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='imagenes/', verbose_name="Imagen", null=True, blank=True)
    descripcion = models.TextField(verbose_name="Descripción", null=True, blank=True)
    activo = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

    def delete(self, using=None, keep_parents=False):
        if self.imagen:
            self.imagen.storage.delete(self.imagen.name)
        super().delete()

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    codigo = models.CharField(max_length=20, unique=True)  # Código del pedido
    fecha_hora = models.DateTimeField(default=timezone.now)  # Fecha y hora del pedido
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relación con el cliente
    descripcion = models.TextField(blank=True, null=True)  # Descripción opcional
    total = models.DecimalField(max_digits=10, decimal_places=2)  # Total del pedido

    def __str__(self):
        return f"Pedido {self.codigo} - {self.cliente.nombre}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')  # Relación con el pedido
    platillo = models.ForeignKey('Platillos', on_delete=models.CASCADE)  # Relación con el platillo
    cantidad = models.PositiveIntegerField()  # Cantidad del platillo
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # Precio unitario
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)  # Subtotal

    def __str__(self):
        return f"Detalle del pedido {self.pedido.codigo} - Platillo {self.platillo.nombre}"