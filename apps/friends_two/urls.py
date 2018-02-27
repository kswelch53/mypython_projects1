#app-level url code:
from django.conf.urls import url, include
from . import views
from django.contrib import admin

urlpatterns = [
    url(r'^friends$', views.index, name='friends'),
    url(r'^add_friend/(?P<user2_id>\d+)$', views.add_friend, name='add_friend'),
    url(r'^remove_friend/(?P<friend_id>\d+)$', views.remove_friend, name='remove_friend'),
    url(r'^user/(?P<id>\d+)$', views.profile, name='profile'),

]
