from django.shortcuts import render, redirect
from product.models import Product
from django.db.models import Q
# Create your views here.


def searchedView(request):
    print(request.GET)
    query = request.GET.get('q')
    print(query)
    if query is not None:
        lookups = Q(title__icontains=query) | Q(
            description__icontains=query)
        searched = Product.objects.filter(lookups).distinct()
    # else:
    #     searched = Product.objects.filter(featured=True)

    context = {
        'qs': searched,
        'searched': query
    }
    if searched.exists():
        return render(request, 'Search/searched.html', context)
    else:
        return render(request, 'Search/error.html')


def error(request):
    return render(request, 'Search/error.html')
