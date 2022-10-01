from django.db import models
from django.contrib.auth.models import User

import uuid 

class SellingMedium(models.Model):
    name = models.CharField(max_length=30)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self) -> str:
        return self.name

# Total amount of shoes sold till now
class Sold(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.user.username} have spent ${self.amount}"

# Total amount of unsold shoes
class UnSold(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.user.username} have not sold ${self.amount}"

class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    product_size = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    buying_price = models.DecimalField(max_digits=10, decimal_places=3)
    selling_price = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    delivery_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    selling_medium = models.ForeignKey(SellingMedium, on_delete=models.SET_NULL, null=True, blank=True)
    is_sold = models.BooleanField(default=False)
    profit = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, default=0)
    created_on = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def save(self, *args, **kwargs):
        if(self.is_sold):  # Danger Zone!!!!!!!!!!!!!
            if(self.selling_price): 
                self.profit = (self.selling_price - self.buying_price) - self.delivery_rate
        super(Inventory, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} have {self.product_name} {self.is_sold}"

    class Meta:
        ordering = ['-updated_at']