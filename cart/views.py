from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart
from product.models import Product
from order.models import Order
from basic.forms import SignInForm, GuestForm
from basic.models import GuestEmail
from billing.models import BillingProfile
from django.contrib.auth import authenticate, login
from address.forms import AddressForm
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
    login_form = SignInForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    # guest_email_id = request.session.get('guest_email_id')
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

    context = {
        'order': order_obj,
        'object': product_,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form
    }
    return render(request, 'cart/checkout.html', context)
