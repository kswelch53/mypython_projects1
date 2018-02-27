from django.db import models
from ..appointments1.models import *

class Task(models.Model):
    user_link=models.ForeignKey(User, related_name="appts", null=True)
    task_name=models.CharField(max_length=50)
    date=models.DateField(default=datetime.today, blank=True)
    time=models.TimeField()
    status=models.CharField(max_length=10, default="Pending")
