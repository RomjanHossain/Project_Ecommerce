# Generated by Django 3.0.2 on 2020-02-12 09:54

from django.db import migrations, models
import product.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, default=69.0, max_digits=19)),
                ('discound_price', models.FloatField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, default='images/no_image.jpg', null=True, upload_to=product.utils.upload_image_path)),
                ('featured', models.BooleanField(default=False)),
                ('times', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
