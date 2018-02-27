from django.db import models
from ..mylibrary1.models import *
from ..mylibrary2.models import *


# Users can catalogue their personal library
class Mybook(models.Model):
    owner_link = models.ForeignKey(User, related_name = "ownerlink", null=True)
    book_link = models.ForeignKey(Book, related_name = "mybooks", null=True)
    title = models.CharField(max_length = 255)
    author = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)


# Users can add books to a Reading list
class Readbook(models.Model):
    reader_link = models.ForeignKey(User, related_name = "readers", null=True)
    book_toread_link = models.ForeignKey(Book, related_name = "readbooks", null=True)
    title = models.CharField(max_length = 255)
    author = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)


# Users can add notes to the books in their lists
class Booknote(models.Model):
    mybook_link = models.ForeignKey(Mybook, related_name="booknotes", null=True)
    readbook_link = models.ForeignKey(Readbook, related_name="readnotes", null=True)
    note = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
