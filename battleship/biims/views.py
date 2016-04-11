import sys
import itertools
import json

from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.utils import timezone
from django.template import loader
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.contrib import messages

from .models import HighVolume, LowVolume, Asset
from .forms import SearchForm
from .helpers import fuzzy_pal

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
def part_lookup(request):
    part_list = HighVolume.objects.all()
    paginator = Paginator(part_list, 10)
    
    page = request.GET.get('page')
    try:
        parts = paginator.page(page)
    except PageNotAnInteger:
        parts = paginator.page(1)
    except EmptyPage:
        parts = paginator.page(paginator.num_pages)

    return render(
            request, 
            'biims/lookup.html', 
            {"parts":parts})

@login_required
def asset_lookup(request):
    asset_list = Asset.objects.all()
    paginator = Paginator(asset_list, 10)

    page = request.GET.get('page')

    try:
        assets = paginator.page(page)
    except PageNotAnInteger:
        assets = paginator.page(1)
    except EmptyPage:
        assets = paginator.page(paginator.num_pages)

    return render(
            request, 
            'biims/lookup.html',
            {"parts":assets})

@login_required
def search(request):
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
    if request.is_ajax:
        high_volume_list = HighVolume.objects.all()
        low_volume_list = LowVolume.objects.all()
        asset_list = Asset.objects.all()

        search_term = request.GET.get('search_term')
        print(search_term)
        response_data = []

        all_items = list(itertools.chain(
            high_volume_list,
            low_volume_list,
            asset_list))

        matches = fuzzy_pal(search_term, all_items)

        #for i in range(len(matches)):
        #    response_data.append({
        #            'name':matches[i][0],
        #            'quantity':matches[i][2].quantity,
        #            'storage_location':matches[i][2].storage_location,
        #            'last_reorder_date':str(matches[i][2].last_reorder_date),
        #            'last_reorder_quantity':matches[i][2].last_reorder_quantity
        #            })
        #    try:
        #        response_data[i]['consumable_location'] = matches[i][2].consumable_location
        #    except:
        #        response_data[i]['consumable_location'] = False

        return render(
                request, 
                'biims/ajax_search.html',
                {"matches":matches})
                #json.dumps(response_data),
                #content_type="application/json")
    else: 
        return HttpResponse(
                json.dumps({'nothing to see':'i dont like you'}),
                content_type="application/json")

