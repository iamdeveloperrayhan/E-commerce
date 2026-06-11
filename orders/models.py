from django.db import models
from accounts.models import CustomerProfile,Address
from products.models import Product
from shared.models import TimestampMixin

# Create your models here.


class Order(TimestampMixin):
    STATUS_CHOICES = [
        ('Pending','pending'),
        ('Paid','paid'),
        ('Shipped','shipped'),
        ('Delivered','delivered'),
        ('Cancelled','cancelled'),
    ]
    customer = models.ForeignKey(to=CustomerProfile,on_delete=models.CASCADE,related_name='orders')
    address = models.ForeignKey(to=Address,on_delete=models.CASCADE,related_name='addresses')
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"Order-{self.id}-{self.customer.user.first_name}_{self.customer.user.last_name}"
    
class OrderItem(TimestampMixin):
    order = models.ForeignKey(to=Order,on_delete=models.CASCADE,related_name='order_items')
    product = models.ForeignKey(to=Product,on_delete=models.CASCADE,related_name='order_items')
    price = models.DecimalField(max_digits=5,decimal_places=2)
    quantity = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"Order Item-{self.order.id}-{self.order.customer.user.first_name}_{self.order.customer.user.last_name}"
