"""mypython_projects URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('apps.app1_landingpage.urls', namespace='app1')),
    url(r'^address_book/', include('apps.address_book.urls', namespace='address_book')),
    url(r'^amadon_store/', include('apps.amadon_store.urls', namespace='amadon_store')),
    url(r'^appointments1/', include('apps.appointments1.urls', namespace='appointments1')),# login register
    url(r'^appointments2/', include('apps.appointments2.urls', namespace='appointments2')),
    url(r'^colorful_words/', include('apps.colorful_words.urls', namespace='colorful_words')),
    url(r'^courses/', include('apps.courses.urls', namespace='courses')),
    url(r'^friends_one/', include('apps.friends_one.urls', namespace='friends_one')),# login register
    url(r'^friends_two/', include('apps.friends_two.urls', namespace='friends_two')),
    url(r'^mylibrary1/', include('apps.mylibrary1.urls', namespace='mylibrary1')),# login register
    url(r'^mylibrary2/', include('apps.mylibrary2.urls', namespace='mylibrary2')),
    url(r'^mylibrary3/', include('apps.mylibrary3.urls', namespace='mylibrary3')),
    url(r'^ninja_gold/', include('apps.ninja_gold.urls', namespace='ninja_gold')),
    url(r'^quotes_one/', include('apps.quotes_one.urls', namespace='quotes_one')),# login register
    url(r'^quotes_two/', include('apps.quotes_two.urls', namespace='quotes_two')),
    url(r'^shoes1/', include('apps.shoes1.urls', namespace='shoes1')),# login register
    url(r'^shoes2/', include('apps.shoes2.urls', namespace='shoes2')),
    url(r'^time_display/', include('apps.time_display.urls', namespace='time_display')),
    url(r'^travelbuddy_one/', include('apps.travelbuddy_one.urls', namespace='travelbuddy_one')),# login register
    url(r'^travelbuddy_two/', include('apps.travelbuddy_two.urls', namespace='travelbuddy_two')),
    url(r'^dashboard1/', include('apps.dashboard1.urls', namespace='dashboard1')),# login register
    url(r'^dashboard2/', include('apps.dashboard2.urls', namespace='dashboard2')),# administrators
    url(r'^dashboard3/', include('apps.dashboard3.urls', namespace='dashboard3')),# all users / profiles / messages
    url(r'^wall_one/', include('apps.wall_one.urls', namespace='wall_one')),# login register
    url(r'^wall_two/', include('apps.wall_two.urls', namespace='wall_two')),
    url(r'^admin/', admin.site.urls),
]
