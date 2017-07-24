from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index), #Goes to main
    url(r'^register$', views.register), #Register user
    url(r'^login$', views.login), #Login user/bring home page
    url(r'^logout$', views.logout), #End session
    url(r'^travels$', views.travels), #Home page
    url(r'^add_trip_page$', views.add_trip_page), #Add trip page w/validation
    url(r'^add_trip$', views.add_trip), #Create query
    url(r'^joined$', views.joined), #Add user to trip
    url(r'^remove$', views.remove), #Reomve user form trip
    url(r'^destination/(?P<trip_id>\d+)$', views.destination), #View trip info
]
