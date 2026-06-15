from django.urls import path
from carts import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('item/<int:pk>/update/', views.update_cart_item, name='update_cart_item'),
]
