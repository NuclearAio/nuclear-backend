# Generated by Django 4.1.1 on 2022-09-25 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_profile', '0003_alter_botprofile_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botprofile',
            name='country',
            field=models.CharField(blank=True, default='United States', max_length=100, null=True),
        ),
    ]
