from email.policy import default
from django.db import models
from django.contrib.auth.models import User

import uuid 

class ProxyType(models.Model):
    proxy_type = models.CharField(max_length=20)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.proxy_type

class ProxyVendor(models.Model):
    name = models.CharField(max_length=20)
    # Number of time this proxy vendor get used, globaly 
    number_of_time_proxy_used = models.PositiveIntegerField(null=True, blank=True)
    total_success = models.PositiveIntegerField(null=True, blank=True)
    number_of_decline = models.PositiveIntegerField(null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True) 

    def save(self, *args, **kwargs):
        if(self.number_of_time_proxy_used==None):  # Danger Zone!!!!!!!!!!!!!
            if(not self.number_of_time_proxy_used): 
                self.number_of_time_proxy_used = 0
                self.total_success = 0
                self.number_of_decline =0
        super(ProxyVendor, self).save(*args, **kwargs)

    def __str__(self):
        return f"Gloably, people used {self.name} proxies {self.number_of_time_proxy_used} times!"

    class Meta:
        ordering = ['-total_success']

class UserProxiesPerformance(models.Model):
    # Filter by week, month, total, year
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proxy_vendor = models.ForeignKey(ProxyVendor, on_delete=models.SET_DEFAULT, default="This vendor has stopped their operations!")
    # Number of time this proxy vendor get used, localy
    # Numner of time proxy from this vendor get used copping.
    number_of_time_vendor_get_used  = models.PositiveIntegerField(null=True, blank=True)
    total_success = models.PositiveIntegerField(null=True, blank=True)
    number_of_decline = models.PositiveIntegerField(null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"user used this vendor's proxy {self.number_of_time_vendor_get_used} times"

    class Meta: 
        ordering =['-total_success']
    # This will be related with reprot/task object


class ProxiesExpense(models.Model):
    # Total spent on proxy till now 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expense = models.PositiveIntegerField(null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return f"{self.user.username} has spent $ {self.expense} on proxies"


class UserProxyExpenseByVendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proxy_vendor = models.ForeignKey(ProxyVendor, on_delete=models.SET_NULL, null=True, blank=False, related_name="proxy_expense_by_vendor")
    # Total spent on this particular proxy
    spent = models.PositiveIntegerField(null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    # View ->  if proxy vendor exsist than update the expence, else -> add the proxy vendor and create a obj in db
    def __str__(self):
        return f"{self.user.username} has spent {self.spent} on {self.proxy_vendor.name}"

              
class Proxy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proxy_vendor = models.ForeignKey(ProxyVendor, on_delete=models.SET_NULL, null=True, blank=True)
    proxy_type = models.ForeignKey(ProxyType, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    ip_address = models.CharField(max_length=50)
    port = models.PositiveSmallIntegerField(null=True, blank=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    cost = models.PositiveSmallIntegerField()
    created_at = models.DateField(null=True, blank=True, auto_now_add=True)
    created_at_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    # Proxy expence by view and proxy_expense by year will be handled on view
    # Get the proxies by year/week then loop through the cost object and them them one by one in fontend

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at_time']