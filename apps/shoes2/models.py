from django.db import models
from ..shoes1.models import *

class Product(models.Model):
    buyer_link=models.ForeignKey(User, related_name="buy_products", null=True, blank=True)
    seller_link=models.ForeignKey(User, related_name="sell_products", null=True, blank=True)
    name=models.CharField(max_length=100)
    date_posted=models.DateField(default=datetime.today)
    date_bought=models.DateField(null=True, blank=True)
    amount=models.DecimalField(decimal_places=2, max_digits=8) # use this for money
    sold=models.BooleanField(default=False, blank=True)
