#app-level url code:
from django.conf.urls import url, include
from . import views

# This is app_three
urlpatterns = [
# route to display user's Bookshelf (displays Mybook objects)
    url(r'^bookshelf_index$', views.bookshelf_index, name='bookshelf_index'),

# route to add a new book to user's Bookshelf (adds Mybook object) and create a new Book object
    url(r'^add_to_bookshelf$', views.add_to_bookshelf, name='add_to_bookshelf'),

# route to add an existing book (Book object) to user's Bookshelf (adds Mybook object)
    url(r'^add_to_bookshelf2/(?P<book_id>\d+)$', views.add_to_bookshelf2, name='add_to_bookshelf2'),

# route to delete from user's Bookshelf (deletes Mybook object)
    url(r'^remove_mybook/(?P<mybook_id>\d+)$', views.remove_mybook, name='remove_mybook'),

# route to display user's Reading List
    url(r'^readinglist_index$', views.readinglist_index, name='readinglist_index'),

# route to add a new book to Reading List
    url(r'^add_to_readinglist$', views.add_to_readinglist, name='readinglist'),

# route to add an existing book to Reading List
    url(r'^add_to_readinglist2/(?P<book_id>\d+)$', views.add_to_readinglist2, name='readinglist2'),

# route to delete from user's Reading List (deletes Readbook object)
    url(r'^remove_readbook/(?P<readbook_id>\d+)$', views.remove_readbook, name='remove_readbook'),
]
