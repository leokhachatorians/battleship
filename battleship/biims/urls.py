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
        url(r'^part_lookup', views.part_lookup, name='part_lookup'),
        url(r'^asset_lookup', views.asset_lookup, name='asset_lookup'),
    ]
