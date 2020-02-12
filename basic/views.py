from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .forms import ContactForm, SignInForm, Registerform, GuestForm
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from product.models import Product
from cart.models import Cart
from basic.models import GuestEmail
from address.forms import AddressForm
# Create your views here.

User = get_user_model()


def home(request):
    AllProduct = Product.objects.all()
    NewProduct = Product.objects.order_by('-times')
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    product_ = cart_obj.products.all()
    context = {
        'title': 'Home',
        'np': NewProduct,
        'ap': AllProduct,
        'object': product_,
        'cart': cart_obj
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
        if request.is_ajax():
            return JsonResponse({'message': 'Thank You for your submission!'})
    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')
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
            try:
                del request.session['guest_email_id']
            except:
                pass
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


def guestform(request):
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        return redirect("checkout")
    return redirect("home")


def SuccessPage(request):
    return render(request, 'basic/success.html', {})
