from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart
from product.models import Product
from order.models import Order
from basic.forms import SignInForm, GuestForm
from basic.models import GuestEmail
from billing.models import BillingProfile
from django.contrib.auth import authenticate, login
# Create your views here.


def cart(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    product_ = cart_obj.products.all()
    total = cart_obj.total
    subtotal = cart_obj.subtotal
    context = {
        'cart': cart_obj,
        'object': product_,
        'total': total,
        'subtotal': subtotal
    }
    return render(request, 'cart/cart.html', context=context)


def cart_update(request):
    print('this is shit but its cool!')
    print(request.POST)
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("cart")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)  # cart_obj.products.add(product_id)
        request.session['cart_total'] = cart_obj.products.count()
        # return redirect(product_obj.get_absolute_url())
    return redirect("cart")


def CheckoutView(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    product_ = cart_obj.products.all()
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart')
    else:
        order_obj, NewOrderObj = Order.objects.get_or_create(cart=cart_obj)
    user = request.user
    billing_profile = None
    login_form = SignInForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get('guest_email_id')

    if user.is_authenticated:
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
            user=user, email=user.email)
    elif guest_email_id is not None:
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(
            email=guest_email_obj.email)
    else:
        pass

    if billing_profile is not None:
        order_qs = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        if order_qs.count() == 1:
            order_obj = order_qs.first()
        else:
            old_order_qs = Order.objects.exclude(
                billing_profile=billing_profile).filter(cart=cart_obj, active=True)
            if old_order_qs.exists():
                old_order_qs.update(active=False)
            order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)

    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(request, username=username, password=password)
    #     print(username, password)
    #     if user is not None:
    #         login(request, user)
    #         print(user.is_authenticated)
    #         return redirect('checkout')
    if request.method == 'POST':
        email = request.POST['email']
        print(email)
        return redirect('checkout')
    context = {
        'order': order_obj,
        'object': product_,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form
    }
    return render(request, 'cart/checkout.html', context)
