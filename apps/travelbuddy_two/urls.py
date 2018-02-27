# Travel Buddy APP 2
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^add_plan$', views.add_plan, name="add_plan"),
    url(r'^destination/(?P<trip_id>\d+)$', views.destination, name="destination"),
    url(r'^join_trip/(?P<trip_id>\d+)$', views.join_trip, name="join_trip"),

]
