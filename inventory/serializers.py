from rest_framework.serializers import ModelSerializer

from .models import (
    SellingMedium,
    Sold,
    UnSold,
    Inventory
)

class SellingMediumSerializer(ModelSerializer):

    class Meta:
        model = SellingMedium
        fields = '__all__'

class SoldSerializr(ModelSerializer):

    class Meta:
        model = Sold,
        fields = '__all__'


class UnSoldSerializer(ModelSerializer):

    class Meta:
        model = UnSold
        fields = '__all__'


class InventorySerializer(ModelSerializer):
    selling_medium = SellingMediumSerializer(read_only=True)
    class Meta:
        model = Inventory
        fields = [
            'id',
            'product_name', 'product_size', 'buying_price', 'selling_price', 
            'delivery_rate', 'selling_medium', 'is_sold',
            'profit'
        ]