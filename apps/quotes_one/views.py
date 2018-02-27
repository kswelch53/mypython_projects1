from django.shortcuts import render, HttpResponse, redirect
from .models import User
# allows flash messages to html
from django.contrib import messages


# displays a form on main.html for users to enter login or registration info
def index(request):
    print("This is index function in quotes_one views.py")
    return render(request, 'quotes_one/index.html')


# logs in user if validations are met
def login(request):
    print("This is login function in app_one views.py")
    # saves user POST data from models method login_user in response_from_models:
    response_from_models = User.objects.login_user(request.POST)
    print("Response from models:", response_from_models)
    if response_from_models['status']:#if true (validations are met):
        #saves user data in session, sends user to 2nd quotes app:
        request.session['user_id'] = response_from_models['user'].id
        request.session['user_alias'] = response_from_models['user'].alias
        return redirect('quotes_two:index')
    else:#returns user to index.html, displays error message:
        messages.error(request, response_from_models['errors'])
        return redirect('quotes_one:index')


# saves a user object if registration validations are met
def register(request):
    print("This is register function in quotes_one views.py")
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
            # index method in app_two will use this:
            request.session['user_id'] = response_from_models['user'].id
            request.session['user_alias'] = response_from_models['user'].alias
            print("Name:", request.session['user_alias'])
# redirects to index method in 2nd quotes app
            return redirect('quotes_two:index')
# 1st app handles only logging in / registering users
        else:
            # add flash messages to html:
            for error in response_from_models['errors']:
                messages.error(request, error)
            # returns to index.html via named route users, index method in views.py
            return redirect('quotes_one:index')

    # if not POST, redirects to index method via named route namespace=users
    else:
        return redirect('quotes_one:index')


def logout (request):
    print("This is logout method in quotes_one views.py")
    request.session.clear()#deletes everything in session
    return redirect('quotes_one:index')
