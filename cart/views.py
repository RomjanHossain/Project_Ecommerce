from django.shortcuts import render
from .models import Cart
# Create your views here.


def cart(request):
    cart_id = request.session.get('cart_id', None)
    # if cart_id is None:
    #     cart_obj = Cart.objects.create(user=None)
    #     request.session['cart_id'] = cart_obj.id
    #     print('New cart Created')
    qs = Cart.objects.filter(id=cart_id)
    if qs.count() == 1:
        print('Cart id exists')
        cart_obj = qs.first()
    else:
        cart_obj = Cart.objects.new(user=request.user)
        request.session['cart_id'] = cart_obj.id
    return render(request, 'cart/cart.html')
