from .views import ProductoListView, ProductoDetailView, MarcaListView, CategoriaListView, PedidoCreateView, ItemPedidoCreateView
from django.urls import path
urlpatterns = [
    path('productos/', ProductoListView.as_view(), name='producto-list'),
    path('productos/<int:pk>/', ProductoDetailView.as_view(), name='producto-detail'),
    path('marcas/', MarcaListView.as_view(), name='marca-list'),
    path('categorias/', CategoriaListView.as_view(), name='categoria-list'),
    
    
]