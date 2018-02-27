#app-level url code:
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^addcourse$', views.addcourse, name="addcourse"),
    url(r'^deletecheck/(?P<course_id>\d+)$', views.deletecheck, name="deletecheck"),
    url(r'^remove/(?P<course_id>\d+)$', views.remove, name="remove"),
]
