from django.db import models
from django.contrib.auth.models import User

import uuid


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    card_number = models.PositiveIntegerField(null=True, blank=True)
    last_four_digit = models.PositiveIntegerField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ['-created_at']
