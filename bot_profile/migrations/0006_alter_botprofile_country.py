# Generated by Django 4.1.1 on 2022-09-26 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_profile', '0005_alter_botprofile_options_botprofile_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botprofile',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
