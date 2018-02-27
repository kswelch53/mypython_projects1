from django.shortcuts import render, HttpResponse, redirect
# from datetime import datetime #this is needed for timenow
import datetime
from time import strftime

def index(request):
    print("This is index method in time_display views.py")
    time_zone = 0
    select = ["selected", "", "", "", "", "", ""]
    # timenow = datetime.now()

    central_time = datetime.datetime.now()
    central_time = central_time.strftime('%B %d, %Y %I:%M %p')
    this_time = central_time

    hawaii_time = datetime.datetime.now() - datetime.timedelta(hours=4)
    hawaii_time = hawaii_time.strftime('%B %d, %Y %I:%M %p')

    alaska_time = datetime.datetime.now() - datetime.timedelta(hours=3)
    alaska_time = alaska_time.strftime('%B %d, %Y %I:%M %p')

    pacific_time = datetime.datetime.now() - datetime.timedelta(hours=2)
    pacific_time = pacific_time.strftime('%B %d, %Y %I:%M %p')

    mountain_time = datetime.datetime.now() - datetime.timedelta(hours=1)
    mountain_time = mountain_time.strftime('%B %d, %Y %I:%M %p')

    eastern_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    eastern_time = eastern_time.strftime('%B %d, %Y %I:%M %p')
    print("Hawaii time is:", hawaii_time)
    print("Alaska time is:", alaska_time)
    print("Pacific time is:", pacific_time)
    print("Mountain time is:", mountain_time)
    print("Central time is:", central_time)
    print("Eastern time is:", eastern_time)

    if 'time_zone' in request.session:
        print("Time zone is:", request.session['time_zone'])
        time_zone = request.session['time_zone']
        if int(time_zone) == 0:
            print("No zone was selected; default is Central time")
            this_time = central_time
            select = ["selected", "", "", "", "", "", ""]

        if int(time_zone) == 1:
            print("Zone is Hawaii time")
            this_time = hawaii_time
            select = ["", "selected", "", "", "", "", ""]

        if int(time_zone) == 2:
            print("Zone is Alaska time")
            this_time = alaska_time
            select = ["", "", "selected", "", "", "", ""]

        if int(time_zone) == 3:
            print("Zone is Pacific time")
            this_time = pacific_time
            select = ["", "", "", "selected", "", "", ""]

        if int(time_zone) == 4:
            print("Zone is Mountain time")
            this_time = mountain_time
            select = ["", "", "", "", "selected", "", ""]

        if int(time_zone) == 5:
            print("Zone is Central time")
            this_time = central_time
            select = ["", "", "", "", "", "selected", ""]

        if int(time_zone) == 6:
            print("Zone is Eastern time")
            this_time = eastern_time
            select = ["", "", "", "", "", "", "selected"]

    context = {
        # "time" : timenow,
        'time': this_time,
        'select': select,
    }
    # print("The time is", timenow)

    return render(request,'time_display/the_time.html', context)


def select_timezone(request):
    print("This is select_timezone method in time_display views.py")
    if request.method == 'POST':
        print("This is select_timezone POST method")
        request.session['time_zone'] = request.POST['time_zone']
        print("Time zone is:", request.session['time_zone'])

        return redirect('time_display:index')

    return redirect('time_display:index')
