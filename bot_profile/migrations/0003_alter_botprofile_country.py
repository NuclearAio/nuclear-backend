# Generated by Django 4.1.1 on 2022-09-25 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_profile', '0002_alter_botprofile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botprofile',
            name='country',
            field=models.CharField(default='United States', max_length=100),
        ),
    ]
