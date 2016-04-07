from django.conf.urls import url

from . import views

urlpatterns = [
        # Index
        url(r'^$', views.login_page, name="login_page"),

        # Options
        url(r'^options/$', views.options, name='options'),

        # User Login/Logout Stuff
        url(r'^login', views.login, name="login"),
        url(r'^logout', views.logout, name="logout"),
    ]
