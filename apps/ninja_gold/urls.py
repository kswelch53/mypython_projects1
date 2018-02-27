
#app-level url code:
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.ninjagold_index, name="index"),
    url(r'^clear$', views.clear, name="clear"),
    url(r'^process_money$', views.process_money, name="process_money"),

]
