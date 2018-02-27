from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date
#importing regex
import re, bcrypt


# Handle logic in the model
# View page will call model method, which is built into the model manager class
class UserManager(models.Manager):
# method to handle user validations
# post_data is the information from request.POST
    def validate_user(self, post_data):
        # dictionary to contain user data from models.py
        response_to_views = {}
        # list to gather up errors:
        errors = []
        print("In model method:", post_data)

        # add validations:
        # Note: This part is often the source of multi-dict key errors
# name
        if not post_data['name']:#python returns an empty string as false
            errors.append('Name is required')
        if not len(post_data['name']) >= 3:
            errors.append('Name must be at least 3 characters')

# username
        if not post_data['username']:#python returns an empty string as false
            errors.append('User name is required')
        if not len(post_data['username']) >= 3:
            errors.append('User name must be at least 3 characters')

# password
        if len(post_data['password']) < 8:
            errors.append('Password must be at least 8 characters')
        if not post_data['password'] == post_data['confirmPW']:
            errors.append('Passwords must match')

# check that submitted username is unique (non-duplicate) before other validations, because users log in with their username
# filter will return false if list is empty, true if not empty
        if self.filter(username = post_data['username']):
            errors.append('Username is already in use')

# checking the errors for failed validations
# if any validations fail, user cannot be logged in
# error messages will be returned
# status and errors are keys in the dictionary response_to_views
        if errors: #failed validations
            response_to_views['status'] = False
            response_to_views['errors'] = errors
        else: #passed validations
            response_to_views['status'] = True

            #hash the password with bcrypt
            hashed_password = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt())

            #create new user, saves data in a variable (user):
            user = self.create(name = post_data['name'], username = post_data['username'], password = hashed_password)
            # user object is saved as a key in list and returned:
            response_to_views['user'] = user
#return response data
        return response_to_views

# finding a user in the database with the user's username:
    def login_user(self, post_data):
        print("This is login_user method in models.py")
        #will be true if username found, false if it isn't:
        response_to_views = {}
        #filter will return only 1 object & won't generate error if username doesn't exist
        user = self.filter(username = post_data['username'])
        print("User:", user)

        if user:#if user username is in the database:
# checks whether submitted password matches one in the database
# submitted pw is hashed with same formula as db password
# because filter returns only 1 object at a time, the user is always user[0]
# bcrypt.checkpw returns a boolean, true or false
            if bcrypt.checkpw(post_data['password'].encode(), user[0].password.encode()):#if boolean is true:
            # user object is saved in response_to_views
                response_to_views['status'] = True
                response_to_views['user'] = user[0]#will be returned & saved in session

            else:#if password is invalid
                response_to_views['status'] = False
                response_to_views['errors'] = "Invalid username/password combination"

        else:#if user username is not found in database:
            response_to_views['status'] = False
            response_to_views['errors'] = "Invalid username"

#return response data
        return response_to_views



class User(models.Model):
    name=models.CharField(max_length=60)
    username=models.CharField(max_length=45)
    password=models.CharField(max_length=25)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

# links UserManager to User, by overwriting the objects hidden key that all models have
    objects = UserManager()
