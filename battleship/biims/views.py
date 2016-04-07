from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.template import loader
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.contrib import messages

def login_page(request):
    if request.user.is_authenticated():
        return render(request, 'biims/options.html')
    return render(request, 'biims/login_page.html')

@login_required
def options(request):
    return render(request, 'biims/options.html')

def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login_user(request, user)
            return redirect('/biims/options')
    else:
        messages.add_message(request, messages.WARNING, 'Invalid Credentials')
        return render(request, 'biims/login_page.html')

def logout(request):
    if request.user.is_authenticated():
        logout_user(request) 
    return render(request, 'biims/login_page.html')
