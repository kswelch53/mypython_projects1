from django.shortcuts import render, HttpResponse, redirect
from .models import User
# allows flash messages to html
from django.contrib import messages

# Note: Registration and login validations are done in models.py

# displays a form on index.html for users to enter login or registration info
def index(request):
    print("This is index function in shoes1 views.py")
    return render(request, 'shoes1/index.html')


# logs in user if validations are met
def login(request):
    print("This is login function in shoes1 views.py")
    # saves user POST data from models method login_user in response_from_models:
    response_from_models = User.objects.login_user(request.POST)
    print("Response from models:", response_from_models)
    if response_from_models['status']:#if true (validations are met):
        #saves user data in session, sends user to 2nd app:
        request.session['user_id'] = response_from_models['user'].id
        request.session['user_first_name'] = response_from_models['user'].first_name
        request.session['user_last_name'] = response_from_models['user'].first_name
        return redirect('shoes2:shoes')
    else:#returns user to index.html, displays error message:
        messages.error(request, response_from_models['errors'])
        return redirect('shoes1:index')


# saves a user object if registration validations are met
def register(request):
    print("This is register function in shoes1 views.py")
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
            # index method in 2nd app will use this:
            request.session['user_id'] = response_from_models['user'].id
            request.session['user_first_name'] = response_from_models['user'].first_name
#redirects to index method in 2nd app
            return redirect('shoes2:shoes')
# 1st app handles only logging in / registering users
        else:
            # add flash messages to html:
            for error in response_from_models['errors']:
                messages.error(request, error)
            # returns to index.html via named route users, index method in views.py
            return redirect('shoes1:index')

    # if not POST, redirects to index method via named route namespace=users
    else:
        return redirect('shoes1:index')


def logout(request):
    request.session.clear()#deletes everything in session
    return redirect('shoes1:index')
