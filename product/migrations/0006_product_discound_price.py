# Generated by Django 3.0.2 on 2020-01-31 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20200130_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discound_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=69.0, max_digits=19),
        ),
    ]
