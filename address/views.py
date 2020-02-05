from django.shortcuts import render, redirect
from billing.models import BillingProfile
from .forms import AddressForm
from .models import Address


def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        "form": form,
        'who': 'Romjan'
    }
    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            instance.billing_profile = billing_profile
            instance.address_type = request.POST.get('address_type', 'shipping')
            instance.save()
        else:
            print("Error here")
            return redirect("cart")
    else:
        print('checkout form finished!')
    return render(request, 'address/form.html', context)


def checkout_address_reuse_view(request):
    # print('runnnnnnnnnnnnn')
    if request.user.is_authenticated:
        if request.method == "POST":
            print(request.POST)
            shipping_address = request.POST.get('shipping_address', None)
            address_type = request.POST.get('address_type', 'shipping')
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            if shipping_address is not None:
                print('shipping address isnot none')
                qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                print(qs, 'this is working')
                if qs.exists():
                    request.session[address_type + "_address_id"] = shipping_address
                    # return redirect(redirect_path)
            else:
                print('shipping_address is none')
    return redirect("ConformO")
