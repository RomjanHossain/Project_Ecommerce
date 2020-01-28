from django.shortcuts import render, redirect
from .forms import ContactForm, SignInForm, Registerform
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
# Create your views here.

User = get_user_model()


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
            return redirect('home')
        else:
            messages.success(request, "Info incorrecet")
            return redirect('login')
    else:
        return render(request, 'basic/auth/login.html', context)


def register(request):
    form = Registerform(request.POST or None)
    context = {
        'title': 'Register',
        'form': form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        new_user = User.objects.create_user(username, email, password)
        messages.success(request, message=f"User {username} created")
        return redirect('login')
    return render(request, 'basic/auth/regi.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def test(request):
    return render(request, 'basic/test.html')
