from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from payments.models import Payment
from orders.models import Order,OrderItem
from accounts.models import CustomerProfile
from django.http import HttpResponse
from django.urls import reverse
import stripe
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = 'sk_test_51SJcXOKhJmVWR5eyf2jZ1D3trk0xMfFVWn9NbrbfY5f0Kzz3pe1d47FFbLPVbpeN7iCFQFpJZnrdhuxSqYmQ6Txo00Z8gQPV46'
STRIPE_WEBHOOK_SECRET = "whsec_gInMNydNXBI1KMnhZS6j6KWawLhOx7x6"

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    try:
        event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                STRIPE_WEBHOOK_SECRET
            )
    except Exception as e:
        return HttpResponse(status=400)
    
    if event["type"] == "checkout.session.completed":
        #TODO: make user cart 0
        pass

    
    if event["type"] == "payment_intent.succeeded":
        print(event)
        # order_id = int(event["data"]["object"]["metadata"]["order_id"])
        # order = Order.objects.get(pk=order_id)
        # order.status = "Paid"
        # order.save()  

    return HttpResponse(status=200)