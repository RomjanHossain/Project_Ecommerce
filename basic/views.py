from django.shortcuts import render, redirect
from .forms import ContactForm, SignInForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def home(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'basic/home.html', context)


def about(request):
    context = {
        'title': 'About Us'
    }
    return render(request, 'basic/about.html', context)


def contact(request):
    contact_form = ContactForm(request.POST or None)
    print(request.POST)
    context = {
        'form': contact_form
    }
    return render(request, 'basic/contact.html', context)


def login_form(request):
    sign_in_form = SignInForm()
    context = {
        'title': 'Sign in',
        'signin': sign_in_form
    }
    if sign_in_form.is_valid():
        username = sign_in_form.cleaned_data.get('username')
        password = sign_in_form.cleaned_data.get('password')
        print(sign_in_form.cleaned_data)
        user = authenticate(request, username=username, password=password)
        print(user.is_authenticated)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print('User not Found')
        context['signin'] = SignInForm()
    return render(request, 'basic/auth/login.html', context)


def register(request):
    context = {
        'title': 'Register'
    }
    return render(request, 'basic/auth/regi.html', context)


def test(request):
    return render(request, 'basic/test.html')
