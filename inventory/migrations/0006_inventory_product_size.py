# Generated by Django 4.1.1 on 2022-09-30 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_alter_inventory_selling_medium'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='product_size',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
    ]