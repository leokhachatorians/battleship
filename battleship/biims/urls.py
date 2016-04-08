from django.conf.urls import url

from . import views

urlpatterns = [
        # Index/Login Page
        url(r'^$', views.login, name="login"),
        url(r'^login$', views.login, name='login'),

        # Options
        url(r'^options/$', views.options, name='options'),

        # User Login/Logout Stuff
        url(r'^logout', views.logout, name="logout"),
        
        # Parts Look Up
        url(r'^parts_lookup', views.parts_lookup, name='parts_lookup'),
    ]
