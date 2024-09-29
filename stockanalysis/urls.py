from django.urls import path
from .views import stocks, StockAutocomplete, stock_detail

urlpatterns = [
    path('stocks', stocks, name='stocks'),
    path('stock-autocomplete', StockAutocomplete.as_view(), name='stock_autocomplete'),
    path('stock-detail/<int:pk>', stock_detail, name='stock_detail')
]
