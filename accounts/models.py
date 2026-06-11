from django.db import models
from django.contrib.auth.models import User
from shared.models import TimestampMixin

# Create your models here.

class Address(TimestampMixin):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code =  models.CharField(max_length=20)
    street =  models.CharField(max_length=255)

    def __str__(self):
        return f"{self.street},{self.city},{self.country}"

class CustomerProfile(TimestampMixin):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='customer_profile')
    phone = models.CharField(max_length=14,null=True,blank=True)
    profile_image = models.ImageField(upload_to='profiles/',blank=True,null=True)
    addresses = models.ManyToManyField(to=Address,blank=True,related_name='customer_profiles')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


"""
address = Address.objects.get(id=1)
customer_profiles = address.customer_profiles
django signals --> django

"""