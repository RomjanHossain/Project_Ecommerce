from django.db import models
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
    postal_code = models.CharField(max_length=4)
    phone = models.CharField(max_length=11)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return "{name}\n, {line1}\n{line2}\n{city}, {postal}\n{country}".format(
            name=self.full_name,
            line1=self.address_line_1,
            line2=self.address_line_2 or "",
            city=self.city,
            postal=self.postal_code,
            country=self.country
        )
