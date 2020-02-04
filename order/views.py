from django.shortcuts import render, redirect
from cart.models import Cart
from billing.models import BillingProfile
from order.models import Order
from address.models import Address
# Create your views here.


def ConformOrder(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    product_ = cart_obj.products.all()
    order_obj = None
    billing_address_id = request.session.get("billing_address_id", None)
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
    print(order_obj)
    if request.method == "POST":
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart__total'] = 0
            del request.session['cart__id']
            return redirect("success")
        else:
            print('holy shit! this is not working')
            print(is_done)
    context = {
        'object': product_, 'order': order_obj
    }
    return render(request, 'cart/conform.html', context)
