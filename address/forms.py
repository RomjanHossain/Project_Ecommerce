from django import forms

from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            # 'billing_profile',
            # 'address_type',
            'full_name',
            'country',
            'city',
            'address_line_1',
            'address_line_2',
            'postal_code',
            'phone',
            'email'

        ]
# # billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
# # address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES)
# fname = models.CharField(max_length=20)
# lname = models.CharField(max_length=20)
# country = models.CharField(max_length=120, default='Bangladesh')
# city = models.CharField(max_length=120)
# address_line_1 = models.CharField(max_length=120)
# address_line_2 = models.CharField(max_length=120, null=True, blank=True)
# postal_code = models.DecimalField(max_digits=6)
# phone = models.DecimalField(max_digits=11)
# email = models.EmailField()
