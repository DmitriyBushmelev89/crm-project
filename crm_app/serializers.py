from rest_framework import serializers
from .models import Client
from .models import Product
from .models import Order


class ClientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    email = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'phone', 'email']


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), required=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'client']

    def validate_price(self, value):
        if value < 1.00:
            raise serializers.ValidationError('Price should not be less than 1')
        return value


class OrderSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), required=True)
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Order
        fields = ['id', 'client', 'products', 'total_price']
        read_only_fields = ['total_price']

    def create(self, validated_data):
        products = validated_data.pop('products')
        validated_data.pop('total_price', None)
        total_price = sum([product.price for product in products])
        order = Order.objects.create(**validated_data, total_price=total_price)
        order.products.set(products)
        return order

    def update(self, instance, validated_data):
        products = validated_data.pop('products', None)

        if products is not None:
            total_price = sum([product.price for product in products])
            instance.total_price = sum([product.price for product in products])
            instance.products.set(products)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
