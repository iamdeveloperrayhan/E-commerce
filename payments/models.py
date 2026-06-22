from django.db import models
from shared.models import TimestampMixin
from orders.models import Order

# Create your models here.
class Payment(TimestampMixin):
    METHOD_CHOICES = [
        ('Card','card'),
        ('Mobile Banking','mobile_banking'),
        ('Cash On Deliver','cash_on_delivery'),
    ]
    order = models.ForeignKey(to=Order,on_delete=models.CASCADE,related_name='payments')
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    stripe_session_id = models.CharField(max_length=255,null=True,blank=True)
    method = models.CharField(max_length=100,choices=METHOD_CHOICES)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment-{self.id}"
