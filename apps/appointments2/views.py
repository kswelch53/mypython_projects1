from django.shortcuts import render, HttpResponse, redirect
from ..appointments1.models import User, UserManager
from ..appointments2.models import Task
import datetime
from time import strftime
from django.contrib import messages


def index(request):
    print("This is index method in appointments2 views.py")
    time_now = datetime.datetime.now()
    time_now.strftime('%B %d, %Y %H:%M %p')
    hour_min = time_now.strftime('%H:%M')
    month_day = time_now.strftime('%B %d')
    year = time_now.strftime('%Y')
    full_date = time_now.strftime('%Y-%m-%d')
    if 'user_id' not in request.session:
        return redirect('appointments1:index')
    else:
        user_id = request.session['user_id']
        this_user = User.objects.get(id=user_id)
        print ("Session user is:", this_user.name)

        todays_date = full_date
        print("Today's date is:", todays_date)

        context = {
            'all_tasks': Task.objects.all().filter(user_link=this_user),
            'hour_min': hour_min,
            'month_day': month_day,
            'year': year,
            # filter by user and date
            # the date filter has to be first, otherwise doesn't work
            'todays_tasks': Task.objects.filter(date=todays_date).filter(user_link=this_user),
            # filter by user and exclude todays_tasks
            'other_tasks': Task.objects.order_by("date").filter(user_link=this_user).exclude(date=todays_date),
        }

        return render(request, 'appointments2/index.html', context)


def add_task(request):
    print("This is add_task method in appointments2 views.py")
    time_now = datetime.datetime.now()
    print("Time is:", time_now)#added
    # get form data
    if request.method == 'POST':
        this_user = User.objects.get(id=request.session['user_id'])
        this_task = request.POST['task_name']
        this_date = request.POST['task_date']
        this_time = request.POST['task_time']

        # check for empty strings
        if (len(this_date) == 0) or (len(this_time) == 0) or (len(this_task) == 0):
            print("Blank form fields")
# error message; redirect
            messages.warning(request, "Form fields must not be left blank")
            return redirect('appointments2:add_task')

        else:# no blank fields, continuing on ...
            # check that form date isn't in the past
            todays_date = time_now.strftime('%Y-%m-%d')
            if this_date < todays_date:
# error message; redirect
                messages.warning(request, "Your appointment cannot be in the past")
                return redirect('appointments2:add_task')

            else:
                # checks whether there are any Task objects
                # if task count is 0, creates object, if count > 0, checks through objects in for-loop
                session_user = User.objects.get(id=request.session['user_id'])# get session user
                user_tasks = Task.objects.filter(user_link=session_user)# get session user's tasks
                task_count = user_tasks.count()
                if task_count == 0:
                    print("There are no appointments for this user yet; creating the first one")
                    # create new Task object
                    new_task = Task.objects.create(user_link=this_user, task_name=this_task, date=this_date, time=this_time, status="Pending")
                    return redirect('appointments2:index')

                # if form date isn't in the past, get form time
                # check for Task object with conflicting date and time
                for task in user_tasks:# checks through Task objects
                    print("task.date is:", task.date, "this_date is", this_date, "task.time is", task.time, "this_time is", this_time)
                    # converts Task object time to same format as form data time, for comparison
                    task_time = task.time.strftime('%H:%M')
                    print("Converted task.time is:", task_time)
                    print("task_time is", task_time, "this_time is", this_time)

                    # compares form data date/time with Task object date/time
                    if str(task.date) == str(this_date) and str(task_time) == str(this_time):
                    # if a match is found
# error message; redirect
                        print("Tasks have the same date and time")
                        messages.warning(request, "You have a conflicting appointment")
                        return redirect('appointments2:add_task')# stays on form page

                    else:# no conflicting appointment
                        this_task = request.POST['task_name']
                        print("Date is:", this_date, ", Time is:", this_time, ", Task is:", this_task)

                        # create new Task object
                        new_task = Task.objects.create(user_link=this_user, task_name=this_task, date=this_date, time=this_time, status="Pending")
                        return redirect('appointments2:index')
    else:# not POST request; redirect to index
        return redirect('appointments2:index')


# updates Task objects
def edit(request, task_id):
    print("This is edit method in appointments2 views.py")

    time_now = datetime.datetime.now()# gets datetime object
    hour_min = time_now.strftime('%H:%M')# time for context, html display

    if request.method == 'POST':
# this_task is the existing Task object, not form data
        this_task = Task.objects.get(id=task_id)
        print("Task to edit is:", this_task.task_name, task_id)
        print("Task status is:", this_task.status)
# checks whether Task object's status is Done
# user can't edit task if status is DONE
# check the object status, not the form status
        if this_task.status == "Done":
            print ("STATUS IS DONE")
# error message
# redirect
            messages.warning(request, "You cannot update a finished task")
            return redirect('appointments2:edit', task_id)

        else: # update Task object
            this_task.name = request.POST['task_name']
            this_task.status = request.POST['status']
            this_task.date = request.POST['task_date']
            this_task.time = request.POST['task_time']
            this_task.save()
            print("Edited task:", this_task.task_name, this_task.status, this_task.date, this_task.time)
            return redirect('appointments2:index')
    else:
        context = {
            'task': Task.objects.get(id=task_id),
            'hour_min': hour_min,
        }

    return render(request, 'appointments2/update.html', context)


def delete(request, task_id):
    print("This is delete method in appointments2 views.py")
    task_to_delete = Task.objects.get(id=task_id)
    print("Task to delete is:", task_to_delete.task_name, task_id)
    task_to_delete.delete()
    return redirect('appointments2:index')
