# Generated by Django 4.1.1 on 2022-09-28 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxy', '0017_alter_proxytype_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proxytype',
            name='proxy_type',
            field=models.CharField(max_length=20),
        ),
    ]
