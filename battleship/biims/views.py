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
def options(request):
    return render(request, 'biims/options.html')

def login(request):
    if request.user.is_authenticated():
        messages.info(
                request,
                'You\'re already logged in',
                extra_tags="login_message")
        return render(request, 'biims/options.html')

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
                return redirect('/biims/options')
        else:
            messages.error(request,
                    'Invalid Credentials',
                    extra_tags="wrong_login")
            return render(request, 'biims/login_page.html')
    else:
        return render(request, 'biims/login_page.html')

def logout(request):
    if request.user.is_authenticated():
        logout_user(request) 
        messages.info(
                request,
                "Logged out succesfully",
                extra_tags="login_message")
    return render(request, 'biims/login_page.html')

@login_required
def search(request):
    """
    The search functionality is quite simple. Utilizing Django's
    lazy querysets, we can create a chained list and pass in the
    all the parts into the paginator. This wont make any excessive
    querys to the database until AFTER we create the page, which
    will make it a total of three queryies if I'm not mistaken.

    Now the SearchForm is our gateway towards making ajax calls
    to our fuzzymatching thing.
    """
    high_volume_list = HighVolume.objects.all()
    low_volume_list = LowVolume.objects.all()
    asset_list = Asset.objects.all()

    form = SearchForm()

    all_items = list(itertools.chain(
        high_volume_list,
        low_volume_list,
        asset_list))

    paginator = Paginator(all_items, 20)

    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(
            request,
            'biims/search.html',
            {
                "parts":items,
                "form":form
            },)

@login_required
def ajax_search(request):
    """
    """
    if not request.is_ajax:
        raise Http404

    if request.is_ajax:
        high_volume_list = HighVolume.objects.all()
        low_volume_list = LowVolume.objects.all()
        asset_list = Asset.objects.all()

        search_term = request.GET.get('search_term')

        all_items = list(itertools.chain(
            high_volume_list,
            low_volume_list,
            asset_list))

        matches = helpers.fuzzy_pal(search_term, all_items)
        return render(
                request, 
                'biims/ajax_search.html',
                {"matches":matches})

def new_item(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST)
        if form.is_valid():
            form_data = helpers.get_new_item_form_data(request)
            print(form_data)
            helpers.add_item_via_form_data(form_data)
            return redirect('biims:options')
    else:
        form = NewItemForm()
    return render(request, 'biims/new_item.html', {'form':form})
    

