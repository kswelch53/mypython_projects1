# urls.py for Appointments app2:

from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^index$', views.index),
    url(r'^add_task$', views.add_task, name="add_task"),
    url(r'^edit/(?P<task_id>\d+)$', views.edit, name="edit"),
    url(r'^delete/(?P<task_id>\d+)$', views.delete, name="delete"),

]
