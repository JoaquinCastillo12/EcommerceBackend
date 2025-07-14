from django.contrib import admin

# Register your models here.

from .models import Categoria, Marca, Producto, Pedido, ItemPedido, Pago

admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(ItemPedido)
admin.site.register(Pago)