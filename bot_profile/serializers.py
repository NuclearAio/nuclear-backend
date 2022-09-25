from rest_framework.serializers import ModelSerializer

from .models import BotProfile

class BotProfileSerializer(ModelSerializer):
    
    class Meta:
        model = BotProfile
        fields = '__all__'
