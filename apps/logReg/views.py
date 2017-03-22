from django.shortcuts import render, redirect
from . models import User
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    context = {
    'hey':User.objects.all()
    }
    return render(request, 'logreg/index.html', context)

def register(request):
    viewsResponse = User.objects.add_user(request.POST)
    print viewsResponse
    if viewsResponse['isRegistered']:
        request.session['user_id'] = viewsResponse['user'].id
        request.session['user_fname'] = viewsResponse['user'].first_name
        return redirect('loginreg:success')
    else:
        for errors in viewsResponse['errors']:
            messages.error(request, errors)
        return redirect('loginreg:index')


def success(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Must be logged in!')
        return redirect('loginreg:index')
    return render(request, 'logreg/success.html')

def login(request):
    viewsResponse = User.objects.login_user(request.POST)
    print viewsResponse
    if viewsResponse['isLoggedIn']:
        request.session['user_id'] = viewsResponse['user'].id
        request.session['user_fname'] = viewsResponse['user'].first_name
        return redirect('loginreg:success')
    else:
        for errors in viewsResponse['errors']:
            messages.error(request, errors)
        return redirect('loginreg:index')

def logout(request):
    request.session.clear()

    return redirect('loginreg:index')