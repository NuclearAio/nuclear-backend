# Generated by Django 4.1.1 on 2022-09-25 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botprofile',
            name='phone_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]