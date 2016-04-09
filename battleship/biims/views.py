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
    paginator = Paginator(part_list, 20)
    
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
    paginator = Paginator(asset_list, 20)

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
