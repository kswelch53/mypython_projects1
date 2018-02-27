from django.shortcuts import render, HttpResponse, redirect
from ..dashboard1.models import User
from .models import *
from django.contrib import messages
import re, bcrypt
import datetime
from time import strftime
# from django.core.urlresolvers import reverse


# accessed by clicking All Users link on home page (app1)
# gets all user objects from database, id of user in session
# renders to all_users.html to display all users, link to edit_profile for session user:
def all_users(request):
    print("This is the all_users method in dashboard3 views.py")
    if 'user_id' not in request.session:
        return redirect('dashboard1:index')
# saving users group in context
    else:
        context = {
            'users': User.objects.all(),
            'session_id': request.session['user_id']
        }
        return render(request, 'dashboard3/all_users.html', context)


# accessed by clicking edit-your-profile link on All Users page
# gets session user's object from database and renders page by id
# renders to edit_profile.html, displays form for editing user name/email
def edit_profile(request, user_id):
    print("This is the edit_profile method in dashboard3 views.py")
    if 'user_id' not in request.session:
        return redirect('dashboard1:index')
    else:
        user = User.objects.get(id=request.session['user_id'])
        print("User is: #", user.id, user.first_name, user.last_name)
        context = {
            'user': User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'dashboard3/edit_profile.html', context)


# route for form data in Edit Info box on edit_profile.html
# allows users to change their name and email
# accessed by Save button, edited data changed in database
def edit_info(request, user_id):
    print
    ("This is the edit_info method in dashboard3 views.py")

# checking id
    print("User ID is:", user_id)

# when the form to edit user name and email is submitted:
    if request.method == "POST":
        print("POST")

# updates session user's object in database and returns to all_users page
        edit_user = User.objects.get(id=user_id)
        print("User is: #", edit_user.id, edit_user.email, edit_user.first_name, edit_user.last_name)
        edit_user.email = request.POST['email']
        edit_user.first_name = request.POST['first_name']
        edit_user.last_name = request.POST['last_name']
        edit_user.save()
        print("Edited user:", edit_user.email, edit_user.first_name, edit_user.last_name)

# ALWAYS REDIRECT after a post request
# the updated user data will appear on the all_users page
        return redirect('dashboard3:all_users')
# will redirect to the same page even if the data isn't updated
    else:
        return redirect('dashboard3:all_users')


# route for form data in Change Password box on edit_profile.html
# allows users to change their password
# accessed by Update Password button, edited data changed in database
def change_pw(request, user_id):
    print("This is the change_pw method in dashboard3 views.py")
    if request.method == 'POST':
        edit_user = User.objects.get(id=user_id)
        print("Editing user:", edit_user.first_name, edit_user.last_name)
        edit_user.password = request.POST['password']
        edit_user.pw_confirm = request.POST['pw_confirm']

# needs password = pwconfirm validation

        #hashes the updated password with bcrypt
        edit_user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        edit_user.save()

# ALWAYS REDIRECT after a post request
        return redirect('dashboard3:all_users')
# will redirect to the same page even if the data isn't updated
    else:
        return redirect('dashboard3:all_users')


# this creates a new user description with form data sent from the Edit Description box on edit_profile.html, and saves it in the User_profile database
def edit_desc(request, user_id):
    print("This is edit_desc method in dashboard3 views.py")
    print("User ID is:", user_id)
    if request.method == 'POST':

# get the user whose profile is to be edited
        this_user = User.objects.get(id=user_id)
        print("Profile of User #", this_user.id, ",", this_user.first_name)

# get the description data from the form
        this_desc = request.POST['description']
        print("Editing description:", this_desc)


# Users can create a description (optional) after they've registered.
# They can also edit an existing description, which is fetched and overwritten.
# Note: Only one description (the first) needs to be created per user. All subsequent ones are updates.
        user_profiles = User_profile.objects.filter(user_link=this_user)
        profile_count = user_profiles.count()
        print("Profile count is", profile_count)
        if profile_count == 0:

# create the User_profile object containing the description
            this_profile = User_profile.objects.create(user_link=this_user, description=this_desc)
            print("User_profile object created:", this_profile.description)
            return redirect('dashboard3:profile', user_id)

        else:
# update the previous description
            this_profile = User_profile.objects.get(user_link=this_user)
            this_profile.description = this_desc
            this_profile.save()
            print(this_profile.description)
            return redirect('dashboard3:profile', user_id)

# anyone who tries to get to a profile page directly should be returned to the dashboard (except it doesn't work)
    else:
        return redirect('dashboard1:index')


# accessed by name-links on both All Users and Manage Users pages
# renders to profile.html, which displays users' profile data by id
# all users can access profile pages and add posts
def profile(request, user_id):
    print("This is the profile method in dashboard3 views.py")


    if request.method == 'POST':
        print("POST", user_id)#message receiver's id

        # get message from request.POST on profile.html
        this_message = request.POST['message']
        print("Message is:", this_message)

        # get sender (user in session) by id
        this_sender = User.objects.get(id=request.session['user_id'])
        print("Sender is:", this_sender.first_name)

        # gets recipient by id
        this_receiver = User.objects.get(id=user_id)
        print("Recipient is:", this_receiver.first_name)

        # saves new message
        new_message = Message.objects.create(post=this_message, send_posts=this_sender, get_posts=this_receiver)
# why can't I use strftime in HTML?
        print(new_message.created_at.strftime('%B %d, %Y'))

        # return redirect('dashboard3:profile', id=user_id)
# note: redirect gives a no-id-match error; message posts when it's removed

    # User object is for user name clicked on (message recipient)
    profiled_user = User.objects.get(id=user_id)
    print("Profiled user is:", profiled_user.first_name)

    try:
        # get user's description (if one exists) from User_profile object
        user_desc = User_profile.objects.get(user_link=profiled_user)
        print("User description:", user_desc)
    except:
        user_desc = ""
        print("User has not submitted a description to profile")

    context = {
    # saving user object in context to display at top of profile page
    # this allows user's name, registration date, id# and email to display
        'profiled_user': profiled_user,

    # this allows user's description, if one exists, to display
        'user_desc': user_desc,

    # Message object contains all posts sent to the above user
    # It also contains a related link to the message sender
        'messages_to_user': Message.objects.filter(get_posts=profiled_user)
    }

    print("Profile page, user id is:", user_id)
    return render(request, 'dashboard3/profile.html', context)
