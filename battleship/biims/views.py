from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.template import loader
from django.contrib.auth import authenticate, login as login_user
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf

def index(request):
    return render(request, 'biims/index.html')

@login_required
def options(request):
    template = loader.get_template('biims/options.html')
    return HttpResponse(template.render(request))

def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login_user(request, user)
            return HttpResponse("Welcome, {}".format(user.username))

    else:
        return HttpResponse("NOPE")

def logout(request):
    return HttpResponse("shit")
