from django.shortcuts import render, HttpResponse, redirect
from .models import User
from ..friends_two.models import Friend
# allows flash messages to html
from django.contrib import messages

# Note: Registration and login validations are done in models.py

# displays a form on index.html for users to enter login or registration info
def index(request):
    print("This is index method in friends_one views.py")
    return render(request, 'friends_one/index.html')


# logs in user if validations are met
def login(request):
    print("This is login function in friends_one views.py")
    # saves user POST data from models method login_user in response_from_models:
    response_from_models = User.objects.login_user(request.POST)
    print("Response from models:", response_from_models)
    if response_from_models['status']:#if true (validations are met):
        #saves user data in session, sends user to friends page:
        request.session['user_id'] = response_from_models['user'].id
        request.session['user_alias'] = response_from_models['user'].alias
        return redirect('friends_two:friends')
    else:#returns user to index.html, displays error message:
        messages.error(request, response_from_models['errors'])
        return redirect('friends_one:index')


# saves a user object if registration validations are met
def register(request):
    print("This is register function in friends_one views.py")
    # this checks that users have submitted form data before proceeding to register route
    if request.method == 'POST':
        print("Request.POST:", request.POST)
        # invokes validations method from the model manager
        # saves user data from models.py in a variable
        # whatever is sent back in the UserManager return statement
        response_from_models = User.objects.validate_user(request.POST)
        print("Response from models:", response_from_models)
        if response_from_models['status']:#if true
            # passed the validations and created a new user
            # user can now be saved in session, by id:
            # index method in friends_two will use this:
            request.session['user_id'] = response_from_models['user'].id
            request.session['user_alias'] = response_from_models['user'].alias
            print("Alias:", request.session['user_alias'])

            # creates a friend objects for each new user registered
            create_friendlist = Friend.objects.create(user = User.objects.get(id=request.session['user_id']))

            return redirect('friends_two:friends')
# 1st app handles only logging in / registering users
        else:
            # add flash messages to html:
            for error in response_from_models['errors']:
                messages.error(request, error)
            return redirect('friends_one:index')

    # if not POST, redirects to index method via named route namespace=users
    else:
        return redirect('friends_one:index')


def logout (request):
    request.session.clear()#deletes everything in session
    return redirect('friends_one:index')
