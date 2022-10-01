from email.policy import default
from django.db import models
from django.contrib.auth.models import User

from bot_profile.models import BotProfile
from card.models import Card
from proxy.models import Proxy
from bot.models import BotSubscription

import uuid 

class Site(models.Model):
    name = models.CharField(max_length=30)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name

# Bot spent on the shoesm till now 
class SpentOnShoes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=5)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.user} spent ${ self.amount} on shoes"

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=30)
    product_size = models.DecimalField(null=True, blank=True, max_digits=3, decimal_places=1)
    product_amount = models.PositiveSmallIntegerField(null=True, blank=True)
    is_success = models.BooleanField(default=True)
    profile = models.ForeignKey(BotProfile, on_delete=models.SET_NULL, null=True, blank=True)
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, blank=True)
    proxy = models.ForeignKey(Proxy, on_delete=models.SET_NULL, null=True, blank=True)
    bot = models.ForeignKey(BotSubscription, on_delete=models.SET_NULL, null=True, blank=True)
    created_on = models.DateField(auto_now_add=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        ordering = ['-created_at']