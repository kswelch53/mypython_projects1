from __future__ import unicode_literals
import re
from django.db import models
from datetime import datetime
from ..friends_one.models import User, UserManager
import time
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


class FriendManager(models.Manager):
    def add_friend(self, user_id, user2_id):
        print("This is addfriend in models.py")

# get object for logged-in user
        user = User.objects.get(id=user_id)
        print("user_id is:", user_id)

# get object for user selected to be new friend
        user2 = User.objects.get(id=user2_id)
        print("user2_id is:", user2_id)

# gets Friend objects by id of logged-in user, new friend user
# defines 2 lists
        friend_list = Friend.objects.get(user=User.objects.get(id=user_id))
        otheruser_list = Friend.objects.get(user = user2)

# uses related name to add new friend to logged-in user's friends list
        friend_list.friends.add(user2)
        print("other_user is:", user2.alias)
# uses related name to add logged-in user to new friend's list
        otheruser_list.friends.add(user)
        print("user is", user.alias)

# returns data to views.py
        return self


    def remove(self, user_id, friend_id):
        print("This is remove in models.py")
        user = User.objects.get(id = user_id)
        friend = User.objects.get(id = friend_id)

        users_list = Friend.objects.get(user=user)
        friends_list = Friend.objects.get(user=friend)

        friends_list.friends.remove(user)
        users_list.friends.remove(friend)
        return self


class Friend(models.Model):
    user = models.ForeignKey(User, related_name="has_friends")
    friends = models.ManyToManyField(User, related_name= "is_friends_with", default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return "<FriendList object: {} {} {}>".format(self.user, self.id, self.friends)
    objects = FriendManager()
