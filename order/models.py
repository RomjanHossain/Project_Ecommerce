from math import fsum
from django.db import models
from cart.models import Cart
from django.db.models.signals import pre_save, post_save
from product.utils import unique_OrderID_generator
from billing.models import BillingProfile
from address.models import Address
# Create your models here.

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
            billing_profile=billing_profile,
            cart=cart_obj,
            active=True, status='created')
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                billing_profile=billing_profile,
                cart=cart_obj)
            created = True
        return obj, created


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)  # AVJH12V
    billing_profile = models.ForeignKey(
        BillingProfile,  on_delete=models.CASCADE, null=True, blank=True)
    # shipping_address
    billing_address = models.ForeignKey(
        Address, related_name="billing_address", on_delete=models.CASCADE, null=True, blank=True)
    # total = models.DecimalField(default=0.00, max_digits=100000, decimal_places=2)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    status = models.CharField(max_length=120, default='Created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=40, max_digits=100000, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100000, decimal_places=2)

    def __str__(self):
        return self.order_id

    objects = OrderManager()

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = fsum([cart_total + shipping_total])
        formatted_total = format(new_total, '.2f')
        # print(new_total)
        self.total = formatted_total
        self.save()
        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        billing_address = self.billing_address
        total = self.total
        if billing_profile and billing_address and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.save()
        return self.status


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_OrderID_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    print("running")
    if created:
        print("Updating... first")
        instance.update_total()


post_save.connect(post_save_order, sender=Order)
