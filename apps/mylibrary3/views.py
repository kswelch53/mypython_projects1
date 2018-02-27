from django.shortcuts import render, HttpResponse, redirect
from ..mylibrary1.models import *
from ..mylibrary2.models import *
from .models import *

# *****************
# BOOKSHELF SECTION
# *****************

# renders to bookshelf_index.html
# displays user's Bookshelf page with Mybook objects
# form page to add books to users' Bookshelf; displays list of all Book objects
def bookshelf_index(request):
    print("This is bookshelf_index method in mylibrary3 views.py")
    if 'user_id' not in request.session:
        return redirect('mylibrary1:index')
    else:
        user_id = request.session['user_id']
        print("User id is", user_id)
        # saves all the Mybook (book) objects linked to the session user
        user_bookshelf = Mybook.objects.filter(owner_link = User.objects.get(id=user_id))
        # counts how many Bookshelf objects the session user has
        bookshelf_count = user_bookshelf.count()
        print("Bookshelf count is:", bookshelf_count)
        if bookshelf_count == 0: # session user has no Mybook objects
            bookshelf_message = "Add a book to your personal library"
        else: # session user has at least 1 Mybook object
            bookshelf_message = "Add another book to your personal library"
        if bookshelf_count == 1:
            item = "book" # not plural if only 1 book
        else:
            item = "books" # plural for book counts of 0 or more than 1
        context = {
            'user_bookshelf': user_bookshelf.order_by('title'),
            'bookshelf_count': bookshelf_count,
            'bookshelf_message': bookshelf_message,
            'item': item,
        }
        return render(request, 'mylibrary3/bookshelf_index.html', context)


# renders to bookshelf_form.html
# creates a new MyBook object and adds it to Bookshelf
# checks whether Book object exists, creates it if it doesn't
def add_to_bookshelf(request):
    print("This is add_to_bookshelf method in mylibrary3 views.py")
    user_id = request.session['user_id']
    this_user = User.objects.get(id=user_id)

    # submits form data on bookshelf_form.html
    if request.method == "POST":
        this_title = request.POST['book_title']
        this_author = request.POST['author']
        print("Book submitted is", this_title, "by", this_author)

        # checks to see if there is already a book by this title and author
        all_books = Book.objects.all()
        count = all_books.count()
        book_exists = "False"

        for book in all_books:
            print("Checking book:", book.title)
            print("Title to match:", this_title)
            if book.title != this_title and book.author != this_author:
                # print("Comparison:", book.title, this_title, book.author, this_author)
                print("Title and author do not match")
            else:
                # print("Comparison:", book.title, this_title, book.author, this_author)
                print("Title and author match; book already exists")
                this_book = Book.objects.get(id=book.id)
                book_exists = "True"
            print("Book exists:", book_exists)
            print("___________________")

        print("All books checked; book exists:", book_exists)
        if book_exists == "True":
            print("Create a Mybook object")
            # create a new MyBook object for session user's List
            this_mybook = Mybook.objects.create(owner_link=this_user, book_link=this_book, title=this_book.title, author=this_book.author)
            print("Mybook created:", this_mybook.title, this_mybook.author)

        else:# if title and author are not already in a Book object
            print("Create a Book object and a Mybook object")
            this_book = Book.objects.create(adds_book=this_user, title=this_title, author=this_author)
            print("Book created:", this_book.title, this_book.author)

            this_mybook = Mybook.objects.create(owner_link=this_user, book_link=this_book, title=this_book.title, author=this_book.author)
            print("Mybook created:", this_mybook.title, this_mybook.author)

        return redirect('mylibrary3:bookshelf_index')# bookshelf_index display's user's Bookshelf

    else: # displays all Book objects on the form page
        all_books = Book.objects.all()
        context = {
            'all_books': all_books.order_by('title'),
        }
        return render(request, 'mylibrary3/bookshelf_form.html', context)


# gets an existing Book object and adds it to Bookshelf (creates Mybook object)
def add_to_bookshelf2(request, book_id):
    print("This is add_to_bookshelf2 method in mylibrary3 views.py")
    user_id = request.session['user_id']
    this_user = User.objects.get(id=user_id)

    # gets selected Book object
    this_book = Book.objects.get(id=book_id)
    print("New Mybook to create is:", this_book.title, "by", this_book.author)

    # creates new Mybook object with the selected Book object
    this_mybook = Mybook.objects.create(owner_link=this_user, book_link=this_book, title=this_book.title, author=this_book.author)

    bookshelf_message = "Add another book to your personal library"
    all_books = Book.objects.all()
    # display all of session user's Mybook objects
    context = {
        'all_books': all_books.order_by('title'),
        'user_bookshelf': Mybook.objects.filter(owner_link=User.objects.get(id=user_id)),
        'bookshelf_message': bookshelf_message,
    }
    return render(request, 'mylibrary3/bookshelf_index.html', context)


# deletes Mybook objects, removing it from session user's Bookshelf
def remove_mybook(request, mybook_id):
    print("This is delete_mybook method in mylibrary3 views.py")
    # delete Mybook object by id
    mybook_to_delete = Mybook.objects.get(id=mybook_id)
    mybook_to_delete.delete()
    return redirect('mylibrary3:bookshelf_index')


# ********************
# READING LIST SECTION
# ********************

# displays user's Reading List, with Readbook objects
def readinglist_index(request):
    print("This is readinglist_index method in mylibrary3 views.py")
    if 'user_id' not in request.session:
        return redirect('mylibrary1:index')
    else:
        user_id = request.session['user_id']
        print("User id is", user_id)
        # saves all the Readbook objects linked to the session user
        user_readinglist = Readbook.objects.filter(reader_link = User.objects.get(id=user_id))
        # counts how many Readbook objects the session user has
        readinglist_count = user_readinglist.count()
        print("Reading list count is:", readinglist_count)
        if readinglist_count == 0:
            readinglist_message = "Create a reading list"
        else:
            readinglist_message = "Add to your reading list"
        if readinglist_count == 1:
            item = "book" # not plural if only 1 book
        else:
            item = "books" # plural for book counts of 0 or more than 1
        context = {
            'user_readinglist': user_readinglist.order_by('title'),
            'readinglist_count': readinglist_count,
            'readinglist_message': readinglist_message,
            # 'bookshelf_message': bookshelf_message,
            'item': item,
        }
        return render(request, 'mylibrary3/readinglist_index.html', context)


# creates a new Book object and adds it to Reading List
def add_to_readinglist(request):
    print("This is add_to_readinglist method in mylibrary3 views.py")
    user_id = request.session['user_id']
    this_user = User.objects.get(id=user_id)

    # submitting form data on readinglist_form.html
    if request.method == 'POST':
        print("Request.POST:", request.POST)
        this_title = request.POST['book_title']
        this_author = request.POST['author']
        print("Book submitted is", this_title, "by", this_author)

        # check to see if there is already a book by this title and author
        all_books = Book.objects.all()
        count = all_books.count()
        book_exists = "False"

        for book in all_books:
            print("Checking book:", book.title)
            print("Title to match:", this_title)
            if book.title != this_title and book.author != this_author:
                # print("Comparison:", book.title, this_title, book.author, this_author)
                print("Title and author do not match")
            else:
                # print("Comparison:", book.title, this_title, book.author, this_author)
                print("Title and author match; book already exists")
                this_book = Book.objects.get(id=book.id)
                book_exists = "True"
            print("Book exists:", book_exists)
            print("___________________")

        # if Book exists, creates a Readbook object only
        # if no Book object, creates the new Readbook and Book objects
        print("All books checked; book exists:", book_exists)
        if book_exists == "True":
            print("Create a Readbook object")
            # create a new Readbook object for session user's List
            this_readbook = Readbook.objects.create(reader_link=this_user, book_toread_link=this_book, title=this_book.title, author=this_book.author)
            print("Readbook created:", this_readbook.title, this_readbook.author)

        else:# if title and author are not already in a Book object
            print("Create a Book object and a Readbook object")
            this_book = Book.objects.create(adds_book=this_user, title=this_title, author=this_author)
            print("Book created:", this_book.title, this_book.author)

            this_readbook = Readbook.objects.create(reader_link=this_user, book_toread_link=this_book, title=this_book.title, author=this_book.author)
            print("Readbook created:", this_readbook.title, this_readbook.author)
        return redirect('mylibrary3:readinglist_index')

    else: # displays all Book objects on the form page
        all_books = Book.objects.all()
        context = {
            'all_books': all_books.order_by('title'),
        }
        return render(request, 'mylibrary3/readinglist_form.html', context)


# gets an existing Book object and adds it to Reading List
def add_to_readinglist2(request, book_id):
    print("This is add_to_readinglist2 method in mylibrary3 views.py")
    user_id = request.session['user_id']
    this_user = User.objects.get(id=user_id)

    # gets selected Book object
    this_book = Book.objects.get(id=book_id)
    print("New Readbook to create is:", this_book.title, "by", this_book.author)

    # creates new Readbook object with the selected Book object
    this_readbook = Readbook.objects.create(reader_link=this_user, book_toread_link=this_book, title=this_book.title, author=this_book.author)

    readinglist_message = "Add to your reading list"
    all_books = Book.objects.all()
    # display all of session user's Readbook objects
    context = {
        'all_books': all_books.order_by('title'),
        'user_readinglist': Readbook.objects.filter(reader_link=User.objects.get(id=user_id)),
        'readinglist_message': readinglist_message,
    }
    return render(request, 'mylibrary3/readinglist_index.html', context)


# deletes Readbook objects, removing it from session user's Reading List
def remove_readbook(request, readbook_id):
    print("This is delete_readbook method in mylibrary views.py")
    # delete Readbook object by id
    readbook_to_delete = Readbook.objects.get(id=readbook_id)
    readbook_to_delete.delete()
    return redirect('mylibrary3:readinglist_index')
