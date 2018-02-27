from django.db import models
from ..quotes_one.models import User

class Quote(models.Model):
# link to user who posts a quote
    post_id=models.ForeignKey(User, related_name="quotes", null=True)
# link to users to add a posted quote
    add_id=models.ManyToManyField(User, related_name="addquotes")
    author=models.CharField(max_length=100)
    quote=models.CharField(max_length=255)
