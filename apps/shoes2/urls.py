from django.conf.urls import url, include
from . import views

# This is app_one
urlpatterns = [
# root route to index method
    url(r'^$', views.shoes, name='shoes'),
    url(r'^shoes$', views.shoes),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^buy/(?P<shoes_id>\d+)$', views.buy, name='buy'),
    url(r'^list_forsale$', views.list_forsale, name='list_forsale'),
    url(r'^remove/(?P<shoes_id>\d+)$', views.remove, name='remove'),
]
