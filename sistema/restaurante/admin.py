from django.contrib import admin
from .models import Platillos, Pedido, DetallePedido
# Register your models here.
admin.site.register(Platillos)
admin.site.register(Pedido)
admin.site.register(DetallePedido)