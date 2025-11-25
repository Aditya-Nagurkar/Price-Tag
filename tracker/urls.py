from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_product, name='add_product'),
    path('update/', views.update_prices, name='update_prices'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('history/<int:product_id>/', views.get_price_history, name='get_price_history'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]
