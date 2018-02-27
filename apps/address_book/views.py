from __future__ import unicode_literals
from .models import User
from django.shortcuts import render, HttpResponse, redirect


def index(request):
    print("This is index method in address_book views.py")
# saving users group in context; users list is displayed on index.html
    context = {
        'users': User.objects.all()
    }
    return render(request, 'address_book/index.html', context)


# routes to page new.html that allows user to create a new user
def new(request):
    print("New method in address_book views.py")
    return render(request, 'address_book/new.html')


# routes to a page that displays data for users by id
def show(request, user_id):
    print("Show method in address_book views.py")
# saving an individual user in context
    context = {
        'user': User.objects.get(id=user_id)
    }
    print("User is:", user_id)
    return render(request, 'address_book/show.html', context)


# Gets User object by id and sends it to edit.html for a user to edit
def edit(request, user_id):
    print("Edit method in views.py: Allows a user on page edit.html to edit an existing user with the given id")
    context = {
        'user': User.objects.get(id=user_id)
    }
    print("user_id is:", user_id)
    return render(request, 'address_book/edit.html', context)


# creates a new User object in the database
def create(request):
    print("Create method in address_book views.py")
    User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
    )
    # returns to display page to display new user
    return redirect('address_book:index')


# routes to a page that asks admin whether he/she wants to delete a user record
def deletecheck(request, user_id):
    print("Deletecheck method in address_book views.py")
    context = {
        "user": User.objects.get(id=user_id)
    }
    return render(request, 'address_book/deletecheck.html', context)


# Deletes a user by id
def destroy(request, user_id):
    print("Destroy method in views.py: Allows a user on page edit.html to remove a user with a given id")
    print("User ID is:", user_id)
    User.objects.get(id=user_id).delete()
    return redirect('address_book:index')


# Sends edited user data to the database from edit.html when the "Update" button is pressed
def update(request, user_id):
    print("Update method in address_book views.py")
# updating user information
    update_user = User.objects.get(id=user_id)
    update_user.first_name = request.POST['first_name']
    update_user.last_name = request.POST['last_name']
    update_user.email = request.POST['email']
    update_user.save()
    return redirect('address_book:index')
