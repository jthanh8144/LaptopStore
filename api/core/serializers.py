from rest_framework import serializers
from . models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        field = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        field = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        field = '__all__'


class CartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartDetail
        field = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        field = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        field = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
