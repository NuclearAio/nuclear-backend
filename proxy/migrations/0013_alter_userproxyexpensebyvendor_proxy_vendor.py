# Generated by Django 4.1.1 on 2022-09-27 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proxy', '0012_alter_userproxyexpensebyvendor_proxy_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userproxyexpensebyvendor',
            name='proxy_vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proxy_expense_by_vendor', to='proxy.proxyvendor'),
        ),
    ]
