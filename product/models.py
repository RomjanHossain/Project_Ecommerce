from django.db import models
from django.utils import timezone
import datetime
from .utils import upload_image_path, unique_slug_generator
from django.db.models.signals import pre_save, post_save

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=19, default=69.00)
    image = models.ImageField(default='images/no_image.jpg',
                              upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    times = models.DateTimeField(auto_now_add=True)

    def was_published_recently(self):
        return self.times >= timezone.now()-datetime.timedelta(days=1)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)
