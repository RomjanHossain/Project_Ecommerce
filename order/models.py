from django.db import models
from cart.models import Cart
from django.db.models.signals import pre_save
from product.utils import unique_OrderID_generator
# Create your models here.

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)  # AVJH12V
    # billing_profile = ?
    # shipping_address
    # billing_address
    # total = models.DecimalField(default=0.00, max_digits=100000, decimal_places=2)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='Created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=40, max_digits=100000, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100000, decimal_places=2)

    def __str__(self):
        return self.order_id


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_OrderID_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)
