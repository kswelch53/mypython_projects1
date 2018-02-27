from django.shortcuts import render, HttpResponse, redirect
from .models import Quote
from ..quotes_one.models import *
from django.contrib import messages

# sends all the quote objects to the quotes page
# on each user's page, excludes the quotes on that user's favorites list
def index(request):
    if 'user_id' not in request.session:
        return redirect('quotes_one:index')
    else:
        print("This is index method in quotes_two views.py")
        quotes = Quote.objects.all()
        context = {
            # 'quotes': Quote.objects.all(),
            # displays session user's favorite quotes:
            'favquotes': Quote.objects.filter(add_id=request.session['user_id']),
            # this excludes favorite quotes from all-quotes list:
            'quotes_minus_favs': quotes.exclude(add_id=request.session['user_id'])

        }
        return render(request, 'quotes_two/quotes.html', context)


# user can add a quote from the main list to his/her favorites list
def add_favquote(request, quote_id):
    print("This is add_favquote method in quotes_two views.py")
    if request.method == "POST":
        print("POST, id is:", quote_id)
        this_user = User.objects.get(id=request.session['user_id'])
        print("User is", this_user.name)

        this_quote = Quote.objects.get(id=quote_id)
        print("Author and quote:", this_quote.author, ":", this_quote.quote)

# Add user to the quote through mtm link
        this_quote.add_id.add(this_user)

        return redirect('quotes_two:index')
    return redirect('quotes_two:index')


# session user can remove quotes from his/her favorites lists
def remove_quote(request, favquote_id):
    print("This is remove_quote method in quotes_two views.py")
    if request.method == "POST":
        print("Favorite quote ID is:", favquote_id)
        this_user = User.objects.get(id=request.session['user_id'])
        this_quote = Quote.objects.get(id=favquote_id)
    # removing a quote using the reverse mtm link
        this_user.addquotes.remove(this_quote)

        return redirect('quotes_two:index')


# user can add a quote to the main list
def contribute_quote(request):
    print("This is contribute_quote method in quotes_two views.py")
    if request.method == "POST":
        print("POST")
        errors = False

# Doing the quote validations here; it takes less code than in models.py
# The 2 validations need to be passed before the author/quote can be added
# author validation
        if not request.POST['author']:#python returns an empty string as false
            messages.error(request, 'Author name is required')
            errors = True
        if not len(request.POST['author']) > 3:
            messages.error(request, 'Author name must be at least 3 characters')
            errors = True

# quote validation
        if not request.POST['quote']:#python returns an empty string as false
            messages.error(request, 'Quote is required')
            errors = True
        if not len(request.POST['quote']) > 10:
            messages.error(request, 'Quote must be at least 10 characters')
            errors = True
        print("Error status is:", errors)

        # this_user has to be the whole user object
        if not errors:
            this_user = User.objects.get(id=request.session['user_id'])
            this_author = request.POST['author']
            this_quote = request.POST['quote']
            print(this_user.name, this_author, this_quote)

            # creating the new quote with the user object
            new_quote = Quote.objects.create(post_id=this_user, author=this_author, quote=this_quote)

            return redirect('quotes_two:index')
        else:
            print("Validations not met")
            return redirect('quotes_two:index')

    return redirect('quotes_two:index')


# displays user pages by id with posted quotes
def users(request, user_id):
    print("This is users method in quotes_two views.py")
# User object of user who posted quote (from a-tag link on quotes page)
    this_user = User.objects.get(id=user_id)
    print("User id is:", user_id)

# gets the user's posted quotes by FK link (use for count)
# (to get the user's added quotes, use mtm link instead of FK)
    user_quotes = Quote.objects.filter(post_id=this_user)

    context = {
    # for display of user alias
        'user': User.objects.get(id=user_id),
    # for display of user's posted quotes
        'quotes': Quote.objects.filter(post_id=user_id),
    # for count of user's posted quotes
        'count': user_quotes.count(),
    }
    return render(request, 'quotes_two/users.html', context)
