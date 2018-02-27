from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^post_message$', views.post_message, name="post_message"),
    url(r'^post_comment/(?P<ms_id>\d+)$', views.post_comment, name="post_comment"),
]
