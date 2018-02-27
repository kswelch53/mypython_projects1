from django.db import models

# Create your models here.
class Course(models.Model):
    name=models.CharField(max_length=100)
    desc=models.CharField(max_length=255)
    date_added=models.DateTimeField(auto_now_add=True)
