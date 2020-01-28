from django.shortcuts import render, redirect
from .forms import ContactForm, SignInForm
from django.contrib import messages
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
    form = SignInForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(username, password)
        if user is not None:
            login(request, user)
            print(user.is_authenticated)
            messages.success(request, "You've logged in Successfully")
            return redirect('home')
        else:
            messages.success(request, "Info incorrecet")
            return redirect('login')
    else:
        return render(request, 'basic/auth/login.html', context)


def register(request):
    context = {
        'title': 'Register'
    }
    return render(request, 'basic/auth/regi.html', context)


def test(request):
    return render(request, 'basic/test.html')


def logout_user(request):
    logout(request)
    messages.success(request, "You're logged Out Successfully")
    return redirect('home')
