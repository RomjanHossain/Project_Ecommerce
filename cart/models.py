from django.db import models
from django.conf import settings
from product.models import Product
# Create your models here.
User = settings.AUTH_USER_MODEL


class CartManger(models.Manager):
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.00, max_digits=100000, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    times = models.DateTimeField(auto_now_add=True)

    objects = CartManger()

    def __str__(self):
        return str(self.id)
