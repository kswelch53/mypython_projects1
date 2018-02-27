#app-level url code in dashboard3:
from django.conf.urls import url, include
from . import views

# app3_messages
urlpatterns = [
# route for rendering all_users.html:
    url(r'^$', views.all_users, name='all_users'),

# route for rendering edit_profile.html:
    url(r'^edit_profile/(?P<user_id>\d+)$', views.edit_profile, name='edit_profile'),

# route for sending form data in edit info box on edit_profile.html:
    url(r'^edit_info/(?P<user_id>\d+)$', views.edit_info, name='edit_info'),

# route for sending form data in change password box on edit_profile.html:
    url(r'^change_pw/(?P<user_id>\d+)$', views.change_pw, name='change_pw'),

# route for sending form data in edit description box on edit_profile.html:
    url(r'^edit_desc/(?P<user_id>\d+)$', views.edit_desc, name='edit_desc'),

    url(r'^profile/(?P<user_id>\d+)$', views.profile, name='profile'),

    # url(r'^user_posts/(?P<user_id>\d+)$', views.user_posts, name='user_posts'),

]
