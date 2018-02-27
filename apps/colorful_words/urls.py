# app-level urls.py for Colorfule Words:
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^addword$', views.addword, name="addword"),
    url(r'^displayword$', views.displayword, name="displayword"),
    url(r'^clear$', views.clear, name="clear"),
]
