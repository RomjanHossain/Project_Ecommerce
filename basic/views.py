from django.shortcuts import render
from .forms import ContactForm
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
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    else:
        contact_form.add_error
    return render(request, 'basic/contact.html', context)


def test(request):
    return render(request, 'basic/test.html')
