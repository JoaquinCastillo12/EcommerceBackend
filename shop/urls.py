from .views import ProductoListView
from django.urls import path
urlpatterns = [
    path('productos/', ProductoListView.as_view(), name='producto-list'),
]