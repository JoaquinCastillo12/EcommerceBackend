from .models import Producto, Categoria, Marca, Pedido, ItemPedido, Pago
from rest_framework import serializers

#Categoria
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

#Marca 
class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nombre']
        
#Producto
class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    marca = MarcaSerializer(read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'categoria', 'marca', 'imagen']

class ProductoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria', 'marca', 'imagen']

class ProductoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria', 'marca', 'imagen']
        read_only_fields = ['id']

#ItemPedido
class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = ['producto', 'cantidad', 'precio_unitario']

class ItemPedidoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = ['pedido', 'producto', 'cantidad', 'precio_unitario']

#Pedido
class PedidoSerializer(serializers.ModelSerializer):
    items = ItemPedidoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = ['id', 'fecha', 'total', 'estado', 'items']
        read_only_fields = ['id', 'fecha']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        pedido = Pedido.objects.create(**validated_data)
        for item_data in items_data:
            ItemPedido.objects.create(pedido=pedido, **item_data)
        return pedido

#Pago
class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['pedido', 'pago_id', 'estado', 'monto', 'fecha_pago']