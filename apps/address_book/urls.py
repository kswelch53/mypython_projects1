from django.conf.urls import url, include
from . import views

urlpatterns = [
# root route to index method
    url(r'^$', views.index, name="index"),
    url(r'new$', views.new, name="new"),
    url(r'^edit/(?P<user_id>\d+)$', views.edit, name="edit"),
    url(r'^show/(?P<user_id>\d+)$', views.show, name="show"),
    url(r'^create$', views.create, name="create"),
    url(r'^deletecheck/(?P<user_id>\d+)$', views.deletecheck, name="deletecheck"),
    url(r'^destroy/(?P<user_id>\d+)$', views.destroy, name="destroy"),
    url(r'^update/(?P<user_id>\d+)$', views.update, name="update"),

]
