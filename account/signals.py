from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import (
    UserProfile
)

def create_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(
			user=instance,
			)
            
		print('Profile Created!') 
    
post_save.connect(create_profile, sender=User)