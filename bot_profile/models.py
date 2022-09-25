from django.db import models
from django.contrib.auth.models import User

import uuid

class BotProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    address_1 = models.TextField()
    address_2 = models.TextField(null=True, blank=True)
    phone_number = models.PositiveIntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True, blank=True)
    zip = models.PositiveIntegerField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4 ,editable=False)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta: 
        ordering =  ['-date_added']

    # At save set self.country=== user.profile.country



