from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from accounts.models import CustomerProfile
from carts.models import Cart
from orders.models import Order, OrderItem


@login_required
@transaction.atomic
def checkout(request):
    if request.method != "POST":
        return redirect('cart_detail')

    customer = get_object_or_404(CustomerProfile, user=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)
    items = cart.cart_items.filter(quantity__gt=0).select_related('variant__product')

    if not items:
        messages.error(request, message="Your cart is empty.")
        return redirect('cart_detail')

    address = customer.addresses.first()
    if address is None:
        messages.error(request, message="Please add a shipping address before checking out.")
        return redirect('address_list')

    total_amount = sum(item.subtotal for item in items)

    order = Order.objects.create(
        customer=customer,
        address=address,
        total_amount=total_amount,
    )

    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.variant.product,
            price=item.variant.product.price,
            quantity=item.quantity,
        )

    return redirect('payment_initiate', order_id=order.pk)
