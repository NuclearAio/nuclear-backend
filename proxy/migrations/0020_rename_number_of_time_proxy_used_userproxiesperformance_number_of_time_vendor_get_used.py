# Generated by Django 4.1.1 on 2022-09-29 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxy', '0019_remove_userproxiesperformance_proxy_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userproxiesperformance',
            old_name='number_of_time_proxy_used',
            new_name='number_of_time_vendor_get_used',
        ),
    ]
