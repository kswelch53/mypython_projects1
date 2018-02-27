from django.db import models
from ..dashboard1.models import User

# Create your models here.
class User_profile(models.Model):
    user_link=models.OneToOneField(User)
    description=models.CharField(max_length=255)

class Message(models.Model):
    post = models.CharField(max_length=255)
    send_posts = models.ForeignKey(User, related_name="senders", null=True)
    get_posts = models.ForeignKey(User, related_name="receivers", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
