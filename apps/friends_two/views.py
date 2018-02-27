from django.shortcuts import render, HttpResponse, redirect
from ..friends_one.models import User, UserManager
from .models import Friend, FriendManager


def index(request):
    if 'user_id' not in request.session:
        return redirect('friends_one:index')
    else:
        print("This is index method in friends_two views.py")
# get session user by id
        user_id = request.session['user_id']
        user = User.objects.get(id = user_id)

        friend_check = Friend.objects.get(user = user)
        print("Friend_list is:", friend_check, user)

        if friend_check.friends.count() == 0:
            print("No friends yet")
            request.session['no_friends'] = "You don't have friends yet"
        if friend_check.friends.count() > 0:
            print("no-friend list is blank")
            request.session['no_friends'] = ""

        allfriends = Friend.objects.get(user = User.objects.get(id=user_id))
        # users = User.objects.exclude(id=request.session['user_id'])
        print("continuing on...")
        context = {

            # displays user's list of friends on friends page
            'friends': allfriends.friends.all(),

            # displays list of other (non-friend) users on friends page
            # 'users': User.objects.exclude(id=request.session['user_id']),
            'users': Friend.objects.all().exclude(user=user).exclude(friends=user),

        }

        return render(request, 'friends_two/friends.html', context)


# user2_id sent in from Add Friend link in friends.html
def add_friend(request, user2_id):
    print("This is add_friend method in app2 views.py")
    print("ID of friend to add is:", user2_id)
    user_id = request.session['user_id']
    this_user = User.objects.get(id=user_id)
    print("User is", this_user.name)

# gets friend object
    # this_friend = User.objects.get(id=user2_id)
    # print("Friend is:", this_friend.name)
    # print("User_id is:", user_id, "user2_id is:", user2_id)

# Creating a friendship between 2 users:
    # this_friend.friend.add(this_user)

# calls add_friend method in models.py, sends 2 ids
    addnewfriend = Friend.objects.add_friend(user_id, user2_id)

# returns to friends page
    return redirect('friends_two:friends')


# friend_id sent in from
def remove_friend(request, friend_id):
    print("This is remove_friend method in friends_two views.py")
    # this_user = User.objects.get(id=request.session['user_id'])
    # this_friend = User.objects.get(id=user2_id)
    # removing a friend using the reverse mtm link
    # this_friend.friends.remove(this_user)

    user_id = request.session['user_id']
    removefriend = Friend.objects.remove(user_id, friend_id)

    return redirect('friends_two:friends')


def profile(request, id):
    print("This is profile method in app2 views.py")
    user = User.objects.get(id=id)
    context = {
    # each user by id
        'user': User.objects.get(id=id),
    }

    return render(request, 'friends_two/user_profile.html', context)
