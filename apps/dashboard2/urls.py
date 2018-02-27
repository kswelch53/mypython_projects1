#app-level url code:
from django.conf.urls import url, include
from . import views

# APP2
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_user$', views.add_user, name='add_user'),
    url(r'^edit_user/(?P<user_id>\d+)$', views.edit_user, name='edit_user'),
    url(r'^edit_password/(?P<user_id>\d+)$', views.edit_password, name='edit_password'),
    url(r'^remove_user_check/(?P<user_id>\d+)$', views.deletecheck, name='check'),
    url(r'^remove_user/(?P<user_id>\d+)$', views.remove_user, name='remove_user')
]
