from email.policy import default
from io import open_code
from django.db import models
from django.contrib.auth.models import User

import uuid

class BotVendor(models.Model):
    name = models.CharField(max_length=20)
    number_of_time_bot_ran = models.PositiveIntegerField(null=True, blank=True)
    total_success = models.PositiveIntegerField(null=True, blank=True)
    number_of_decline = models.PositiveIntegerField(null=True, blank=True)
    success_rate = models.PositiveSmallIntegerField(null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True) 

    def save(self, *args, **kwargs):
        if(self.number_of_time_bot_ran==None):  # Danger Zone!!!!!!!!!!!!!
            if(not self.number_of_time_bot_ran): 
                self.number_of_time_bot_ran = 0
                self.total_success = 0
                self.number_of_decline =0
        elif(self.number_of_time_bot_ran==0):
            self.success_rate = 0
        else:
            self.success_rate = (self.total_success/self.number_of_time_bot_ran) * 100
        super(BotVendor, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} have success rate of {self.success_rate} persent"

    class Meta:
        ordering = ['-success_rate']


class UserBotPerformance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bot_vendor = models.ForeignKey(BotVendor, on_delete=models.CASCADE)
    # Number of time this proxy vendor get used, localy
    number_of_time_bot_ran = models.PositiveIntegerField(null=True, blank=True)
    total_success = models.PositiveIntegerField(null=True, blank=True)
    number_of_decline = models.PositiveIntegerField(null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.total_success}"

    class Meta: 
        ordering =['-total_success']


class BotSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bot_vendor = models.ForeignKey(BotVendor, on_delete=models.SET_NULL, null=True, blank=False)
    # Total spent on this particular proxy
    one_time_cost =  models.PositiveIntegerField(null=True, blank=True)
    # cost per month 
    cost = models.PositiveIntegerField(null=True, blank=True)
    still_subscribed = models.BooleanField(default=True, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.user.username} has spent {self.cost} on {self.bot_vendor.name}"

