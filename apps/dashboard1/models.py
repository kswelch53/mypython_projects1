from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date
import re, bcrypt
import random

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_user(self, post_data):
        print("This is UserManager in models.py", post_data)
        response_to_views = {}
        errors = []
        print("In model method:", post_data)

#first name validations:
        if not post_data['first_name']:
            errors.append('First name is required')
            print("Errors:", errors)
        if not len(post_data['first_name']) >= 2:
            errors.append('First name must be at least 2 characters')

#last name validations:
        if not post_data['last_name']:
            errors.append('Last name is required')
        if not len(post_data['last_name']) >= 2:
            errors.append('Last name must be at least 2 characters')

#email validations:
        # sends post_data into regex to be checked for match
        if not EMAIL_REGEX.match(post_data['email']):
            errors.append('Enter a valid email')

#Password validations:
        if len(post_data['password']) < 8:
            errors.append('Password must be at least 8 characters')
        if not post_data['password'] == post_data['confirmPW']:
            errors.append('Passwords must match')

# check that submitted email is unique (non-duplicate) before other validations, because users log in with their emails
# filter will return false if list is empty, true if not empty
        if self.filter(email = post_data['email']):
            errors.append('Email is already in use')

#fail/pass validations:
        if errors:#failed validations
            response_to_views['status'] = False
            response_to_views['errors'] = errors
            print("Errors:", errors)

        else:#passed validations
            response_to_views['status'] = True

            #create a user level
            try: # checks that at least one User object exists
                User.objects.get(id=1)
                user_level = random.randint(0,9)
                if user_level == 0:
                    user_level = 1
                print("User level is:", user_level)
            except: # makes the first user registered an administrator
                user_level = 9
                print("User level is", user_level)
            #hash the password with bcrypt
            hashed_password = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt())

            #create a new user object
            user = self.create(first_name = post_data['first_name'], last_name = post_data['last_name'], email = post_data['email'], password = hashed_password, level = user_level)

            print("User is:", user)
            response_to_views['user'] = user
        return response_to_views

# finding a user in the database with the user's email:
    def login_user(self, post_data):
        print("This is login_user method in models.py")
        #will be true if email found, false if it isn't:
        response_to_views = {}
        #filter will return only 1 object & won't generate error if email doesn't exist
        user = self.filter(email = post_data['email'])
        print("User:", user)
        if user:#if user email is in the database:
            # checks whether submitted password matches one in the database
            # submitted pw is hashed with same formula as db password
            # because filter returns only 1 object at a time, the user is always user[0]
            # bcrypt.checkpw returns a boolean, true or false

            if bcrypt.checkpw(post_data['password'].encode(), user[0].password.encode()):#if boolean is true:
# the 3 lines below are a temporary bypass for changing forgotten passwords
# change user's password in shell, note out bcrypt line above, then enable lines below
# after signing in as user, restore lines as they were, then change user's password in program
            # user16=User.objects.get(id=16)
            # if post_data['password'] == user16.password:
                # print("Passwords match")

            # user object is saved in response_to_views
                response_to_views['status'] = True
                response_to_views['user'] = user[0]#will be returned & saved in session

            else:#if password is invalid
                response_to_views['status'] = False
                response_to_views['errors'] = "Invalid email/password combination"

        else:#if user email is not found in database:
            response_to_views['status'] = False
            response_to_views['errors'] = "Invalid email"

#return response data
        return response_to_views


# Create your models here.
class User(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=25)
    level = models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects = UserManager()
