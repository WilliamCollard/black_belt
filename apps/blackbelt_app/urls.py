from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^new_user$', views.new_user),
    url(r'^user_dash$', views.user_dash),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add_trip$', views.add_trip),
    url(r'^joined/(?P<trip_id>\d+)$', views.joined),
    url(r'^show/(?P<trip_id>\d+)$', views.show),
    url(r'^delete/(?P<trip_id>\d+)$', views.delete),
    url(r'^create_trip$', views.create_trip),
]
