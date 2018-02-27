from django.db import models
from ..mylibrary1.models import User, UserManager
from datetime import datetime, date


class Book(models.Model):
    # links Book object to User object of person who created it
    adds_book = models.ForeignKey(User, related_name = "books")# related name should be users
    title = models.CharField(max_length = 255)
    author = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)


class Review(models.Model):
    # links Review object to User object of person who created it
    user_link = models.ForeignKey(User, related_name = "userlink")
    # links Review object to Book object of book being reviewed
    book_link = models.ForeignKey(Book, related_name = "booklink")
    review = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
