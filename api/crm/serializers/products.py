"""Products Serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from api.crm.models import Product, Category, Price, Inventory

# Serializers
from .delivery import DeliveriesForProductRetrieve


# Category
class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class DetailCategorySerializer(serializers.ModelSerializer):
    used_in = serializers.SerializerMethodField('get_count_used_in_products')

    def get_count_used_in_products(self, category):
        qs = Product.objects.filter(category=category.id)
        serializer = ShortDetailProduct(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'used_in'
        )


class CategoryShortToListProduct(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name'
        )


# Inventory
class UpdateIventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = (
            'uuid',
            'stock',
            'alert_stock'
        )


class InventoyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


# Products

class ShortDetailProduct(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name'
        )


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ListProductsSerializer(serializers.ModelSerializer):
    normal_price = serializers.SerializerMethodField('get_price')
    stock_quantiy = serializers.SerializerMethodField('get_stock')
    category = CategoryShortToListProduct()

    def get_price(self, product):
        qs = Price.objects.filter(product=product, is_normal_price=True).first()
        serializer = PriceModelSerializer(instance=qs, many=False)
        return serializer.data['price']

    def get_stock(self, product):
        qs = Inventory.objects.filter(product=product).first()
        serializer = InventoyModelSerializer(instance=qs, many=False)
        return serializer.data['stock']

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'category',
            'is_stock',
            'stock_quantiy',
            'normal_price',
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryShortToListProduct()
    stock = serializers.SerializerMethodField('get_stock')
    normal_price = serializers.SerializerMethodField('get_normal_price')
    deliveries_prices = serializers.SerializerMethodField('get_prices_deliveries')
    other_prices = serializers.SerializerMethodField('get_other_prices')

    def get_stock(self, product):
        qs = Inventory.objects.filter(product=product).first()
        serializer = InventoyModelSerializer(instance=qs, many=False)
        return serializer.data

    def get_normal_price(self, product):
        qs = Price.objects.filter(product=product, is_normal_price=True).first()
        serializer = NormalPriceSerializer(instance=qs, many=False)
        return serializer.data

    def get_prices_deliveries(self, product):
        qs = Price.objects.filter(product=product, is_delivery=True)
        serializer = DeliveryPriceSerializer(instance=qs, many=True)
        return serializer.data

    def get_other_prices(self, product):
        qs = Price.objects.filter(product=product, is_normal_price=False, is_delivery=False)
        serializer = NormalPriceSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'is_stock',
            'description',
            'category',
            'stock',
            'normal_price',
            'deliveries_prices',
            'other_prices'
        )


# Prices
class CreatePriceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'

    def validate(self, data):

        get_product = Price.objects.filter(product=data['product'], is_normal_price=True).first()
        if get_product and 'is_normal_price' in data:
            raise serializers.ValidationError('Ya existe un precio normal para este producto')

        if 'delivery' in data and 'is_delivery' not in data:
            raise serializers.ValidationError('Debes indicar que el precio es de delivery antes de elegir un servicio de delivery')

        if 'is_delivery' in data and 'delivery' not in data:
            raise serializers.ValidationError('Debes indicar el servicio de delivery')

        if 'is_delivery' in data and 'is_normal_price' in data:
            raise serializers.ValidationError('No puedes ingresar un precio con ambas opciones')

        return data


class UpdateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = (
            'title',
            'price'
        )


class PriceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'


class NormalPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = (
            'id',
            'title',
            'price'
        )


class DeliveryPriceSerializer(serializers.ModelSerializer):
    delivery = DeliveriesForProductRetrieve()

    class Meta:
        model = Price
        fields = (
            'id',
            'title',
            'delivery',
            'price'
        )
