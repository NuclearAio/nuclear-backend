# Generated by Django 4.1.1 on 2022-10-07 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_delete_spentonbot'),
    ]

    operations = [
        migrations.AddField(
            model_name='botvendor',
            name='success_rate',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
