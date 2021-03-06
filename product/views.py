from django.shortcuts import render, get_object_or_404
from .models import Product
from cart.models import Cart
from analytics.signals import object_viewed_signal
# Create your views here.

# def NewProduct(request):
#     queryset = Product.objects.order_by('-times')
#     context = {
#     'qs':queryset
#     }
#     return render(request, )


def ProductView(request):
    NewProduct = Product.objects.order_by('-times')
    AllProduct = Product.objects.all()
    context = {
        'np': NewProduct,
        'ap': AllProduct
    }
    # print(context['qs'])
    return render(request, 'basic/test.html', context)


def featured_view(request, pk=None, *args, **kwargs):
    try:
        obj = Product.objects.get(id=pk, featured=True)
    except Product.DoesNotExist:
        print('this is not featured')
        obj = ''
    context = {
        'object': obj
    }
    object_viewed_signal.send(instance.__class__, instance=obj, request=request)
    return render(request, 'product/detail.html', context)


# def slug_view(request, slug, *args, **kwargs):
#     instance = get_object_or_404(Product, slug=slug)
#     context = {
#         'object': instance
#     }
#     return render(request, "product/detail.html", context)


def DeatilView(request, slug, *args, **kwargs):
    instance = get_object_or_404(Product, slug=slug)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context = {
        'p': instance,
        'cart': cart_obj
    }
    object_viewed_signal.send(instance.__class__, instance=instance, request=request)
    return render(request, 'product/detail.html', context)


def QuickView(request, slug, *args, **kwargs):
    instance = get_object_or_404(Product, slug=slug)
    context = {
        'p': instance
    }
    object_viewed_signal.send(instance.__class__, instance=instance, request=request)
    return render(request, 'product/quickview.html', context)
