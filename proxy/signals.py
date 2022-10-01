from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import (
    ProxiesExpense
)

@receiver(post_save, sender=User)
def create_user_proxy_expense(sender, instance, created, **kwargs):
    if(created):
        ProxiesExpense.objects.create(user=instance)
    
    
@receiver(post_save, sender=User)
def save_user_proxy_expense(sender, instance, **kwargs):
        instance.proxiesexpense.save()