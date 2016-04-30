import sys
import itertools
import json

from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.utils import timezone
from django.template import loader
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import HighVolume, LowVolume, Asset
from .forms import SearchForm, NewItemForm
from . import helpers

@login_required
def options(request, template='biims/options.html'):
    return render(request, template)

def login(request, 
          invalid_template='biims/login_page.html',
          succesful_template='biims/options.html'):
    if request.user.is_authenticated():
        messages.info(
                request,
                'You\'re already logged in',
                extra_tags="login_message")
        return render(request, succesful_template)

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login_user(request, user)
                messages.info(
                    request,
                    'Welcome {}'.format(request.user.username),
                    extra_tags="login_message")
                return render(request, succesful_template)
        else:
            messages.error(request,
                    'Invalid Credentials',
                    extra_tags="wrong_login")
            return render(request, invalid_template)
    else:
        return render(request, invalid_template)

def logout(request, template='biims/login_page.html'):
    if request.user.is_authenticated():
        logout_user(request) 
        messages.info(
                request,
                "Logged out succesfully",
                extra_tags="login_message")
    return render(request, template)

@login_required
def search(request, template='biims/search.html'):
    """
    The search functionality is quite simple. Utilizing Django's
    lazy querysets, we can create a chained list and pass in the
    all the parts into the paginator. This wont make any excessive
    querys to the database until AFTER we create the page, which
    will make it a total of three queryies if I'm not mistaken.

    Now the SearchForm is our gateway towards making ajax calls
    to our fuzzymatching thing, and that is displayed in 'ajax_search()'
    """
    form = SearchForm()

    all_items = helpers.combine_models_for_pagination()
    paginator = Paginator(all_items, 20)

    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, template,
                {
                 "items":items,
                 "form":form
                },)

@login_required
def ajax_search(request, template='biims/ajax_search.html'):
    """
    """
    if not request.is_ajax:
        raise Http404

    if request.is_ajax:
        search_term = request.GET.get('search_term')

        all_items = helpers.combine_models_for_pagination()
        matches = helpers.fuzzy_pal(search_term, all_items)
        return render(request, template, {"matches":matches})

@login_required
def new_item(request, template='biims/new_item.html'):
    if request.method == 'POST':
        form = NewItemForm(request.POST)
        if form.is_valid():
            form_data = helpers.get_new_item_form_data(request)
            if helpers.check_if_item_exists(form_data):
                messages.info(
                        request,
                        'That item already exists',
                        extra_tags="item_exists_error")
                return render(request, template, {'form':form})
            else:
                helpers.add_item_via_form_data(form_data)
                messages.info(
                        request,
                        'The item was saved.',
                        extra_tags='item_saved')
                return redirect('/new_item')
    else:
        form = NewItemForm()
    return render(request, template, {'form':form})
    
@login_required
def request_item_removal(request, item_name=None, template='biims/item_removal.html'):
    item = helpers.check_if_valid_item(item_name)
    item.name = item.name.replace('-',' ')
    url = request.META.get('HTTP_REFERER', '/')
    return render(request, template, {
        'item':item,
        'url':url})
