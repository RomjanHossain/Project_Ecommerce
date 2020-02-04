from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart
from product.models import Product
from order.models import Order
from basic.forms import SignInForm, GuestForm
from basic.models import GuestEmail
from billing.models import BillingProfile
from django.contrib.auth import authenticate, login
from address.forms import AddressForm
from address.models import Address
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
    billing_address_id = request.session.get("billing_address_id", None)
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart')
    login_form = SignInForm()
    guest_form = GuestForm()
    form = AddressForm(request.POST or None)
    billing_form = AddressForm()
    guest_email_id = request.session.get('guest_email_id')
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
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

        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id:
            order_obj.save()
    if request.method == "POST":
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart__id'] = 0
            del request.session['cart__id']
            return redirect("success")

    context = {
        'order': order_obj,
        'object': product_,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        "form": form,
        'billing_form': billing_form
    }
    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()
            request.session[address_type + "_address_id"] = instance.id
            print(address_type + "_address_id")
            return redirect('ConformO')
        else:
            return redirect("cart")
    else:
        print('this shit aint valid')
    return render(request, 'cart/checkout.html', context)
