from django.urls import path
from payments import views
from payments import webhook

urlpatterns = [
    path('<int:order_id>/initiate/', views.payment_initiate, name='payment_initiate'),
    path('<int:order_id>/success/', views.payment_success, name='payment_success'),
    path('<int:order_id>/cancel/', views.payment_cancel, name='payment_cancel'),
    path('webhook/',webhook.stripe_webhook,name='stripe_webhook')

]
