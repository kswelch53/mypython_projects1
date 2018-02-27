from django.shortcuts import render, HttpResponse, redirect
from ..mylibrary1.models import User, UserManager
from .models import Book, Review
from datetime import datetime, date


# See My_Library in Github projects folder for the latest version
# Has zero-checks that prevent errors when there are no Book objects, fewer than 3 Review objects

# displays main page Books
def index(request):
    print("This is index method in mylibrary2 views.py")
    all_books = Book.objects.all() # added for zero-check
    book_count = all_books.count() # added for zero-check
    if 'user_id' not in request.session:
        return redirect('mylibrary1:index')


# PREVENTS ERROR: This section comes into play if no Book objects exist
    elif book_count == 0: # added for zero-check
        context = {
            'books': all_books,
        }
        return render(request, 'mylibrary2/books.html', context)


    else:
        # fetches session user
        this_user = User.objects.get(id=request.session['user_id'])
        # fetches all the books this user has added
        user_books = Book.objects.filter(adds_book=this_user)
        # counts the number of books this user has added
        user_bookcount = user_books.count()
        print("User is:", this_user.name, "User book count is:", user_bookcount)

        # fetches the 3 most recent reviews for display
        latest3_reviews = Review.objects.order_by("-created_at")[:3]

        # set up empty arrays
        latest3_books = []
        books_reviewed = []
        books_not_reviewed = []
        books_reviewed_notlast3 = []

# find Book objects with 3 most recent reviews
        for review in latest3_reviews:
            book_id = review.book_link.id
            book_reviewed = Book.objects.get(id=book_id)
            # latest 3 books reviewed
            latest3_books.append(book_reviewed)

# find Book objects that have reviews (to be excluded from not-reviewed list)
        all_books = Book.objects.all()
        for book in all_books:
            all_reviews = book.booklink.all() # gets all Review objects via Book reverse link to Review
            review_count = all_reviews.count() # counts how many Review objects linked to each Book
            each_book = Book.objects.get(id=book.id) # gets each Book by id
            if review_count == 0: # each Book without a review is appended to array books_not_reviewed
                no_reviews = Book.objects.get(id=book.id)
                books_not_reviewed.append(each_book)
                print("Book has no reviews:", book.title)
            else: # each Book with a review is appended to array books_reviewed
                books_reviewed.append(each_book)
                print("Book has a review:", book.title)

        # filters books with 3 latest reviews from list
        all_books_notlast3 = all_books.exclude(id=latest3_books[0].id).exclude(id=latest3_books[1].id).exclude(id=latest3_books[2].id)
        for book in all_books_notlast3:
            all_reviews = book.booklink.all() # gets all Review objects via Book reverse link to Review
            review_count = all_reviews.count() # counts how many Review objects linked to each Book
            each_book = Book.objects.get(id=book.id) # gets each Book by id
            if review_count == 0: # each Book without a review is appended to array books_not_reviewed; already done
                # no_reviews = Book.objects.get(id=book.id)
                # books_not_reviewed.append(each_book)
                print("Book has no reviews:", book.title)
            else:
                books_reviewed_notlast3.append(each_book) # each Book with a review is appended to array books_reviewed_notlast3
                print("Book has a review:", book.title)

        context = {
            'books': all_books,

            # displays all Book objects except those with the 3 latest reviews
            'books_notlast3': all_books.exclude(id=latest3_books[0].id).exclude(id=latest3_books[1].id).exclude(id=latest3_books[2].id),

            # all books with reviews (Book objects are in an array)
            'books_reviewed': books_reviewed,
            'books_reviewed_notlast3': books_reviewed_notlast3,

            # all Book objects without reviews
            'books_not_reviewed': books_not_reviewed,

            'reviews': latest3_reviews,
        }
        return render(request, 'mylibrary2/books.html', context)


# adds a Book object if it does not already exist
def add_book(request):
    print("This is add_book method in mylibrary2 views.py")
    if request.method == "POST":
        print("Post")
        this_user = User.objects.get(id=request.session['user_id'])
        print("User is", this_user.name)
        this_title = request.POST['book_title']
        pick_author = request.POST['pick_author']
        print("Book submitted is", this_title, "by", pick_author)

        # checks whether author is from form data or selector option (pick_author)
        if len(pick_author) > 0:
            this_author = pick_author
        else:
            this_author = request.POST['add_author']

        this_review = request.POST['review']
        this_rating = request.POST['rating']
        print(this_title, this_author, this_review, this_rating)

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
                this_book = Book.objects.get(id=book.id) #this_book is the matching book
                book_exists = "True"
            print("Book exists:", book_exists)
            print("___________________")

        print("All books checked; book exists is", book_exists)
        if book_exists == "False": # create a Book and a Review
            print("Create a book and a review")

            # create a Book object with ForeignKey linked to User
            new_book = Book.objects.create(adds_book=this_user, title=this_title, author=this_author)
            new_review = Review.objects.create(user_link=this_user, book_link=new_book, review=this_review, rating=this_rating)
            print("Book and review created; book is:", new_book.title, ", and review is:", new_review.review)

        else: # book already exists; create a review only
            print("Create a review only")
            # Review linked to Book and User with ForeignKeys
            new_review = Review.objects.create(user_link=this_user, book_link=this_book, review=this_review, rating=this_rating)
            print("Review created:", new_review.review)
        return redirect('mylibrary2:index')

    else: # not POST
        return render(request, 'mylibrary2/add_book.html')


# adds a Review to a Book
def add_review(request, id):# id of Book object
    print("This is add_review method in mylibrary2 views.py")
    print("ID is", id)
    this_user = User.objects.get(id=request.session['user_id'])
    print("User is", this_user.name)
    this_book = Book.objects.get(id=id)
    print("Book is:", this_book.title)

    if request.method == "POST":
        print("Post")
        this_review = request.POST['review']
        this_rating = request.POST['rating']
        print("Rating is:", this_rating, "Review is", this_review)

# creates a Review object
        new_review = Review.objects.create(user_link=this_user, book_link=this_book, review=this_review, rating=this_rating)
        print("Review created!")
        return redirect('mylibrary2:index')

# displays reviews
    else:
        # filters Review objects linked to the selected book
        reviews_for_book = Review.objects.filter(book_link=this_book)

        for review in reviews_for_book:
            # user who submitted the review
            print("Reviewer name and ID is", review.user_link.name, review.user_link.id)
            user_id = request.session['user_id']
            # book linked to the review
            book_title = review.book_link.title
            book_id = review.book_link.id
            print("Book title and id are:", book_title, book_id)

            # confirms in terminal whether reviewer and session user are the same person
            if review.user_link.id == user_id:
                print("IDs are equal", review.user_link.id, user_id)
            else:
                print("IDs are not equal", review.user_link.id, user_id)

        context = {
            'book': Book.objects.get(id=id),
            'reviews': reviews_for_book,
            'delete_review': delete_review,
        }
        return render(request, 'mylibrary2/add_review.html', context)


# displays page with Reviews posted by session user
def users(request, user_id):
    print("This is users method in mylibrary2 views.py")
    this_user = User.objects.get(id=user_id)
    print("User is:", this_user, "User ID is:", user_id)

    # fetches all reviews created by this user
    user_reviews = Review.objects.filter(user_link=this_user)

    # fetches user's 3 most recent reviews for display
    latest3_reviews = user_reviews.order_by("-created_at")[:3]
    # checks whether reviewer and session user are the same person
    # need to attach delete_review label to session-user reviews
    # need to attach empty string to other reviews

    context = {
        'user': User.objects.get(id=user_id),
        # 'books_created': Book.objects.filter(adds_book=this_user),

        # sends over the latest 3 reviews
        'books_reviewed': latest3_reviews,
        'count': user_reviews.count(),
    }
    return render(request, 'mylibrary2/users.html', context)


# lets session user delete Reviews they have created
def delete_review(request, review_id):
    print("This is delete_review method in mylibrary2 views.py")

    # these 4 lines are for terminal display, not functionality
    this_user = User.objects.get(id=request.session['user_id'])
    this_review = Review.objects.get(id=review_id)
    reviewer = User.objects.get(userlink=this_review)
    print("User is:", this_user.name, "Review is", this_review.review, "Reviewer is:", reviewer.name)

    # deletes a selected review
    review_to_delete = Review.objects.get(id=review_id)
    review_to_delete.delete()
    print("Review deleted!")
    # gets id of selected Book object
    id = review_to_delete.book_link.id
    return redirect('mylibrary2:add_review', id)
