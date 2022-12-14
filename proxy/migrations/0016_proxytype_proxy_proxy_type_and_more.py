# Generated by Django 4.1.1 on 2022-09-28 18:09

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('proxy', '0015_alter_proxy_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyType',
            fields=[
                ('proxy_type', models.CharField(max_length=10)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='proxy',
            name='proxy_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='proxy.proxytype'),
        ),
        migrations.AddField(
            model_name='userproxiesperformance',
            name='proxy_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='proxy.proxytype'),
        ),
    ]
