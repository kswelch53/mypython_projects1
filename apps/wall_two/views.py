from django.shortcuts import render, HttpResponse, redirect
from ..wall_one.models import *
from .models import Message, Comment


# renders home page, sends all user objects to it
def index(request):
    print("This is index method in walls_two views.py")
    context = {
        'users': User.objects.all(),
    }
    return render(request, 'wall_two/index.html', context)


# saves new message submitted by the user
# redirects to the home page
def post_message(request):
    print("This is post_message method in wall_two views.py")

    if request.method == "POST":
        print("POST, messages")
        new_message = request.POST['message']
        print("Message is:", new_message)

        # this_user is the session user
        this_user = User.objects.get(id=request.session['user_id'])
        print(this_user.id, this_user.first_name, this_user.last_name, this_user.email)

        saved_message = Message.objects.create(user_link=this_user, message=new_message)
        print(saved_message)

        return redirect('wall_two:post_message')
    return redirect('wall_two:index')


# gets message that the user is posting on, by its id that is sent through the form
def post_comment(request, ms_id):
    print("This is post_comment method in wall_two views.py")

    if request.method == "POST":
        print("POST, comments")
        print("Message id sent from html is:", ms_id)
        ms_id = int(ms_id)
        new_comment = request.POST['comment']
        print("Submitted comment is:", new_comment)

        this_user = User.objects.get(id=request.session['user_id'])
        print("Session user is:", this_user.id, this_user.first_name, this_user.last_name, this_user.email)

        this_message = Message.objects.get(id=ms_id)
        print("Message linked to id is:", this_message.message)

# creating Comment object
        saved_comment = Comment.objects.create(user_link=this_user, message_link=this_message, comment=new_comment)
        print(saved_comment)

    return redirect('wall_two:index')
