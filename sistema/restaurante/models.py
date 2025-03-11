from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Platillos(models.Model):
    id = models.AutoField(primary_key=True)
    platillo = models.CharField(max_length=100, verbose_name='Título')
    imagen = models.ImageField(upload_to='imagenes/', verbose_name="Imagen", null=True)
    descripcion = models.TextField(verbose_name="Descripción", null=True)
    activo = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return f"Título: {self.platillo} - Descripción: {self.descripcion}"

    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()

class Pedido(models.Model):
    codigo_pedido = models.AutoField(primary_key=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    identificacion_persona = models.CharField(max_length=50)
    descripcion = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido {self.codigo_pedido} - Total: {self.total}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    codigo_platillo = models.ForeignKey(Platillos, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle de Pedido {self.pedido.codigo_pedido} - Platillo: {self.codigo_platillo.platillo}"
