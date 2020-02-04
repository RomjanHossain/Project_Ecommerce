from django.shortcuts import render, redirect
from billing.models import BillingProfile
from .forms import AddressForm


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
    return render(request, 'address/form.html', context)
