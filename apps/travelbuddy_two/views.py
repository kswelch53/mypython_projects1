from django.shortcuts import render, HttpResponse, redirect
# links model to view functions
from ..travelbuddy_one.models import User
from .models import Trip
# allows flash messages to html
from django.contrib import messages
from datetime import datetime, date

# Note: Registration and login validations are done in models.py
# users is the named route for app1; travel is the named route for app2


def index(request):
    if 'user_id' not in request.session:
        return redirect('travelbuddy_one:index')
    else:
        print("This is index function in app_two views.py")
        print("Username is:", request.session['username'], request.session['user_id'])
        user_id = request.session['user_id']

# This saves all the created trips in context and renders them on index.html
# Variable trips contains objects to be displayed by the for-loop in index.html
        context = {
# lists all the trips for the session user
# includes both trips the user has planned and joined
            'trips': Trip.objects.filter(joiner_id=user_id).order_by('start_date'),
# Lists all the trips planned by others, excluding those the session user has joined
            'all_trips': Trip.objects.exclude(joiner_id=user_id).order_by('start_date'),
        }

# users who are logged in are directed to the dashboard:
    return render(request, 'travelbuddy_two/index.html', context)


# adds a travel plan (creates Trip object)
# redirects to index method for html display
# Note: Always redirect after creating an object
def add_plan(request):
    print("This is add_plan function in app_two views.py")
    if request.method == "POST":
        print("method=POST")
        print("Username is:", request.session['username'])
        print(request.POST['destination'], request.POST['plan'], request.POST['start_date'], request.POST['end_date'])

# saves post data in variables
        this_dest = request.POST['destination']
        this_plan = request.POST['plan']
        this_start = request.POST['start_date']
        this_end = request.POST['end_date']

# check for blank form fields
        if len(this_dest) == 0 or len(this_plan) == 0 or len(this_start) == 0 or len(this_end) == 0:
# error message; redirect
            print("Please fill out all form fields")
            messages.warning(request, "Form fields must not be left blank")
            return redirect('travelbuddy_two:add_plan')

# checks that start_date is in the future
        if this_start < str(date.today()):
            datestring = str(date.today())
            print("Today's date is:", datestring)
            print("Trip start date is:", this_start)
# error message; redirect
            print("The start date cannot be in the past")
            messages.warning(request, "Your start date cannot be in the past")
            return redirect('travelbuddy_two:add_plan')
# checks that end_date is after start_date
        if this_end < this_start:
            print("Trip start date is", this_start)
            print("Trip end date is", this_end)
# error message; redirect
            print("The end date cannot be before the start date")
            messages.warning(request, "Your end date cannot be before the start date")
            return redirect('travelbuddy_two:add_plan')

# saves session user id in variable
        this_user_id = request.session['user_id']
# uses session user id to fetch User object
        this_user = User.objects.get(id=this_user_id)
        print("Ready to create a new trip!")

# creates Trip object with User object related name
        this_trip = Trip.objects.create(user_id=this_user, destination=this_dest, plan=this_plan, start_date=this_start, end_date=this_end)
# adds trip creator to the Trip object as a trip joiner
# I haven't figured out how else to display all of a user's planned trips together (created and joined) on index page table 1
        this_trip.joiner_id.add(this_user)

        return redirect('travelbuddy_two:index')
        # return render(request, 'app_two/add_plan.html', context)

# back to add_plan.html if user is not logged in
    else:
        return render(request, 'travelbuddy_two/add_plan.html')


# routes to destination.html, which displays info about a user's trip
def destination(request, trip_id):
    print("This is destination function in travelbuddy_two views.py")
    print("Trip ID:", trip_id)

# note: I called the ForeignKey to the creating user user_id, which is confusing
# user_id is what I use for the session user; FK needs to be called user_link
    this_user_id = request.session['user_id']
    this_trip = Trip.objects.get(id=trip_id) # gets the selected trip by id
    trip_planner_id = this_trip.user_id.id # gets id of trip creator through ForeignKey

# finds all users who joined a trip, filtered by reverse mtm link
    trip_joiners = User.objects.filter(jointrips=Trip.objects.get(id=trip_id))

    context = {
        'trip': Trip.objects.get(id=trip_id), # selected trip
        'trip_planner': User.objects.get(id=trip_planner_id), # creator of selected trip
        'trip_joiners': trip_joiners.exclude(id=trip_planner_id), # all who joined the trip except the trip planner
    }
    return render(request, 'travelbuddy_two/destination.html', context)


# user can join another user's trip
def join_trip(request, trip_id):
    print("This is join_trip function in travelbuddy_two views.py")
    print("Trip ID:", trip_id)

# gets the logged-in user
    this_user_id = request.session['user_id']
    this_user = User.objects.get(id=this_user_id)
    print("Traveler is:", this_user.name)

# gets the trip the user wants to join (trip_id sent from the link)
    this_trip = Trip.objects.get(id=trip_id)
    print("Join trip:", this_trip.destination, this_trip.plan)

# adds the trip to session user's travel itinerary by creating a new trip object linked to the user
# user_id=this_user is the user object of the logged-in user
    this_trip.joiner_id.add(this_user)
    print(this_trip.joiner_id.name)
    return redirect('travelbuddy_two:index')
