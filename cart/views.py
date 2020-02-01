from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart
from product.models import Product
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
