
from .models import Producto, Pedido, Categoria, Marca, ItemPedido
from .serializers import ProductoSerializer, PedidoSerializer, CategoriaSerializer, MarcaSerializer, ItemPedidoSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

class ProductoListView(ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
    
class ProductoDetailView(RetrieveAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
    
class MarcaListView(ListAPIView):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [AllowAny]
    
class CategoriaListView(ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]
    
class PedidoCreateView(CreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [AllowAny]
    
class ItemPedidoCreateView(CreateAPIView):
    queryset = ItemPedido.objects.all()
    serializer_class = ItemPedidoSerializer
    permission_classes = [AllowAny]
    
# views.py
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

PAYPAL_CLIENT_ID = 'AbZiPWiIad2ELQ9r9_mC8LLTgm3CYx0Rk7szow44mktmYyKhITxCHv7BW6OBsFELk84qOvJi5L6BotDb'
PAYPAL_SECRET = 'EOc2A18TPC72fVvS-ORPlJyMLFgCs-JTfCyKHstVhEjTBel-btkB1XQWJjF-rD_t-iRcScmNmrpH1_VJ'
BASE_URL = 'https://api-m.sandbox.paypal.com'

def get_paypal_token():
    res = requests.post(
        f'{BASE_URL}/v1/oauth2/token',
        auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
        headers={'Accept': 'application/json'},
        data={'grant_type': 'client_credentials'}
    )
    return res.json().get('access_token')

@api_view(['POST'])
def create_order(request):
    token = get_paypal_token()
    precio = request.data.get('precio')
    nombre = request.data.get('nombre')
    res = requests.post(
        f'{BASE_URL}/v2/checkout/orders',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        json={
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "USD",
                    "value": f"{precio}"
                },
                "description": nombre
            }]
        }
    )
    return Response({'orderID': res.json()['id']})

@api_view(['POST'])
def capture_order(request):
    order_id = request.data.get('orderID')
    token = get_paypal_token()
    res = requests.post(
        f'{BASE_URL}/v2/checkout/orders/{order_id}/capture',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    )
    return Response(res.json())
