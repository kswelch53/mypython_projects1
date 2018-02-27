#app-level url code:
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^add_book$', views.add_book, name="add_book"),
    url(r'^add_review/(?P<id>\d+)$', views.add_review, name="add_review"),
    url(r'^users/(?P<user_id>\d+)$', views.users, name="users"),
    url(r'^delete_review/(?P<review_id>\d+)$', views.delete_review, name="delete_review"),

]
