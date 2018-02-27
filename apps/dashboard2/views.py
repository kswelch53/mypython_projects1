from django.shortcuts import render, HttpResponse, redirect
from ..dashboard1.models import User
from django.contrib import messages
import re, bcrypt

# dashboard1 is login-registration app
# dashboard2 is administrators app
# dashboard 3 is all users app

# displays user group on manage_users.html
# accessed by clicking Administrators link on home page
def index(request):
    print("This is the index method in dashboard2 views.py")

# If not logged in, users will be returned to the home page
    if 'user_level' not in request.session:
        return redirect('dashboard1:index')
# Only level 9 users can access manage_users.html
    elif request.session['user_level'] == 9:
        print("User is an administrator")

    # saving users group in context
        context = {
            'users': User.objects.all()
        }

        all_users=User.objects.all()
        return render(request, 'dashboard2/manage_users.html', context)
# Logged-in users who are not a level 9 will be returned to the home page
    else:
        print("User is not an administrator. User level is:", request.session['user_level'])
        return redirect('dashboard1:index')


# displays add_user.html; admins can add a new user
def add_user(request):
    print("This is the add_users method in dashboard2 views.py")
    if request.method == 'POST':
        response_from_models = User.objects.validate_user(request.POST)
        print("Response from models:", response_from_models)
        return redirect('dashboard2:index')
    return render(request, 'dashboard2/add_user.html')


# Administrators can edit individual users by clicking Edit link on manage_users.html
def edit_user(request, user_id):
    print("This is the edit_users method in dashboard2 views.py")

# updates user object with data from form on edit_user.html
    if request.method == 'POST':
        # fetches User object to be edited
        edit_user = User.objects.get(id=user_id)
        print("Editing user:", edit_user.first_name, edit_user.last_name)

        # checks for blank fields, redirects if found
        if len(request.POST['email']) == 0:
            print("email field is blank")
            messages.warning(request, "Email field is blank")# works without the extra_tags
            return redirect('dashboard2:edit_user', user_id)
        if len(request.POST['first_name']) == 0:
            print("first_name field is blank")
            messages.warning(request, "First name field is blank", extra_tags='alert')
            return redirect('dashboard2:edit_user', user_id)
        if len(request.POST['last_name']) == 0:
            print("last_name field is blank")
            messages.warning(request, "Last name field is blank", extra_tags='alert')
            return redirect('dashboard2:edit_user', user_id)
        if len(request.POST['level']) == 0:
            print("user level field is blank")
            messages.warning(request, "User level field is blank", extra_tags='alert')
            return redirect('dashboard2:edit_user', user_id)
        else:
        # checks for duplicate email, redirects
            other_users = User.objects.exclude(id=user_id)# excludes user's current email from search
            for user in other_users:
                if user.email == request.POST['email']:# checks for duplicate in other_users
                    print("duplicate email")
# this is meant to alert admin to a duplicate email with a message on edit_user.html
# but the error message appears on login.html instead
                    messages.warning(request, "Email is already in use", extra_tags='alert')
                    # redirects to same page, clearing info fields
                    return redirect('dashboard2:edit_user', user_id)
                else:# if submitted email change is not a duplicate
                    print("email is unique")
                    edit_user.email = request.POST['email']# saves submitted email as user's new email
                    edit_user.first_name = request.POST['first_name']
                    edit_user.last_name = request.POST['last_name']
                    edit_user.level = request.POST['level']
                    edit_user.save() # saves form data in database

# returns all user objects, including the edited object, to the page for display
            context = {
                'users': User.objects.all(),
            }
            return render(request, 'dashboard2/manage_users.html', context)
# displays page before editing
# gets user object to be edited
    context = {
        'user': User.objects.get(id=user_id)
    }
    print("edit_user method, user is:", user_id)

    return render(request, 'dashboard2/edit_user.html', context)


# Admins can update password
def edit_password(request, user_id):
    print("This is the edit_password method in dashboard2 views.py")
    if request.method == 'POST':
        edit_user = User.objects.get(id=user_id)
        print("Editing user:", edit_user.first_name, edit_user.last_name)
        edit_user.password = request.POST['password']
        edit_user.pw_confirm = request.POST['pw_confirm']

# password = pwconfirm validation; aborts if passwords don't match
        if not edit_user.password == edit_user.pw_confirm:
            redirect('dashboard2:index')
        else:
            #hashes the updated password with bcrypt
            edit_user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            edit_user.save()

    # returns all user objects, including the edited object, to the page for display
            context = {
                'users': User.objects.all()
            }
            return render(request, 'dashboard2/manage_users.html', context)
    else:
        context = {
            'user': User.objects.get(id=user_id)
        }
        return render(request, 'dashboard2/edit_user.html', context)


# asks Administrators whether they want to delete a user object
def deletecheck(request, user_id):
    print("This is deletecheck function in dashboard2 views.py")
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'dashboard2/delete_user.html', context)


#deletes a user from the database
def remove_user(request, user_id):
    print("This is the remove_user method in dashboard2 views.py")
    User.objects.get(id=user_id).delete()
    context = {
        'users': User.objects.all()
    }
    return render(request, 'dashboard2/manage_users.html', context)
