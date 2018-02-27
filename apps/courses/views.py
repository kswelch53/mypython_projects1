from __future__ import unicode_literals
from .models import Course
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

# displays a form on index.html that allows users to create and delete courses
def index(request):
    print("This is index function in courses views.py")
    context = {
        "courses": Course.objects.all()
    }
    return render(request, 'courses/index.html', context)


# lets user add a course and description to the database
# Displays the course on index.html
def addcourse(request):
    print("This is addcourse function in courses views.py")
# Length validations here
    print("name length is", len(request.POST['name']))
    print("desc length is", len(request.POST['desc']))
    if (len(request.POST['name']) >= 5) & (len(request.POST['desc']) >= 15):
    # add courses here
        Course.objects.create(
            name=request.POST['name'],
            desc=request.POST['desc'],
        )
        print("This is if statement")
        return redirect('courses:index')

    # Else statement comes into play if length validations aren't met:
    # This setup give only one error message; if both are invalid, only the first (class name) will show
    else:
        print("This is else statement")
    # Both inputs are too short
        if (len(request.POST['name']) < 5) & (len(request.POST['desc']) <= 15):
            print("Class name and description are too short")
            messages.warning(request, "Class name must be at least 5 characters and description must be at least 15 characters")

    # Description meets validation; only class name is invalid
        elif (len(request.POST['desc']) > 15):
            print("Class name is too short")
            messages.warning(request, "Class name must be at least 5 characters")

    # Only description is invalid
        else:
            print("Description is too short")
            messages.warning(request, "Description must be at least 15 characters")
        return redirect('courses:index')


# sends user to delete.html to ask if they want to delete a course
def deletecheck(request, course_id):
    print("This is deletecheck function in views.py")
    context = {
        "course": Course.objects.get(id=course_id)
    }
    return render(request, 'courses/deletecheck.html', context)


# Deletes a course or not depending on user response to delete.html form
def remove(request, course_id):
    print("This is remove function in views.py")
    Course.objects.get(id=course_id).delete()
    return redirect('courses:index')
