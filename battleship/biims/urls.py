from django.conf.urls import url

from . import views

urlpatterns = [
        # Index/Login Page
        url(r'^$', views.login, name="login"),
        url(r'^login$', views.login, name='login'),

        # Options
        url(r'^options$', views.options, name='options'),

        # User Login/Logout Stuff
        url(r'^logout', views.logout, name="logout"),
        
        # Search
        url(r'^search', views.search, name="search"),
        url(r'^ajax_search', views.ajax_search, name="ajax_search"),

        # New Item
        url(r'^new_item', views.new_item, name='new_item'),

        # Remove Item Request
        #url(r'^remove_item/', views.request_item_removal, name='remove_item_plain'),
        url(r'^remove_item/(?P<item_name>[-\w]+)', views.request_item_removal, name='remove_item'),
    ]
