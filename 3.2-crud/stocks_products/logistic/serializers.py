from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "description"]


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ["product", "quantity", "price"]


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ["id", "address", "positions"]

    def create(self, validated_data):
        positions = validated_data.pop("positions")

        stock = super().create(validated_data)
        for position in positions:
            position.update(stock=stock)
            StockProduct.objects.create(**position)
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop("positions")
        stock = super().update(instance, validated_data)
        for position in positions:
            positions_prod = StockProduct.objects.filter(
                stock=stock, product=position.get("product")
            )
            if positions_prod:
                positions_prod.update(**position)
            else:
                position.update(stock=stock)
                StockProduct.objects.create(**position)
        return stock
