from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from payments.models import Payment
from orders.models import Order,OrderItem
from accounts.models import CustomerProfile
from django.http import HttpResponse
from django.urls import reverse
import stripe

stripe.api_key = 'sk_test_51SJcXOKhJmVWR5eyf2jZ1D3trk0xMfFVWn9NbrbfY5f0Kzz3pe1d47FFbLPVbpeN7iCFQFpJZnrdhuxSqYmQ6Txo00Z8gQPV46'

@login_required
def payment_initiate(request,order_id):
    customer = get_object_or_404(CustomerProfile,user=request.user)
    order = get_object_or_404(Order,pk=order_id)
    items = OrderItem.objects.filter(order=order).select_related('product')

    line_items = []
    for item in items:
        line_items.append(
            {
                'price': item.product.stripe_price_id,
                'quantity': int(item.quantity),
            }
        )

    session = stripe.checkout.Session.create(
        payment_intent_data={
            'metadata': {'order_id': order.pk}
        },
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success', args=[order.pk])),
        cancel_url=request.build_absolute_uri(reverse('payment_cancel', args=[order.pk])),
        metadata={'order_id': order.pk}
        )

    return redirect(session.url, permanent=False)


@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id, customer__user=request.user)
    return render(
        request=request,
        template_name='payments/success.html',
        context={'order': order},
    )


@login_required
def payment_cancel(request, order_id):
    order = get_object_or_404(Order, pk=order_id, customer__user=request.user)
    return render(
        request=request,
        template_name='payments/cancel.html',
        context={'order': order},
    )
