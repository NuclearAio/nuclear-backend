# Generated by Django 4.1.1 on 2022-09-29 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0006_alter_report_product_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='product_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
    ]
