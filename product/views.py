from django.shortcuts import render, get_object_or_404
from .models import Product
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


def product_detail_view(request, pk=None, *args, **kwargs):
    instance = get_object_or_404(Product, pk=pk)
    context = {
        'object': instance
    }
    return render(request, "product/detail.html", context)


def featured_view(request, pk=None, *args, **kwargs):
    try:
        obj = Product.objects.get(id=pk, featured=True)
    except Product.DoesNotExist:
        print('this is not featured')
        obj = ''
    context = {
        'object': obj
    }
    return render(request, 'product/detail.html', context)


def slug_view(request, slug, *args, **kwargs):
    instance = get_object_or_404(Product, slug=slug)
    context = {
        'object': instance
    }
    return render(request, "product/detail.html", context)
