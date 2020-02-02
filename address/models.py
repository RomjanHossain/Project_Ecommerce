from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
    ('both', 'Both'),
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    full_name = models.CharField(max_length=20)
    country = models.CharField(max_length=120, default='Bangladesh')
    city = models.CharField(max_length=120)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    postal_code = models.DecimalField(max_digits=6, decimal_places=4)
    phone = PhoneNumberField()
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return str(self.billing_profile)
