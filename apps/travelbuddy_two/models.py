from django.db import models
from ..travelbuddy_one.models import *

class Trip(models.Model):
    user_id=models.ForeignKey(User, related_name="trips", null=True)#should be user_link
    joiner_id=models.ManyToManyField(User, related_name="jointrips")#should be joiner_link
    destination=models.CharField(max_length=100)
    start_date=models.DateField(default=datetime.today, blank=True)
    end_date=models.DateField(default=datetime.today, blank=True)
    plan=models.CharField(max_length=255)
