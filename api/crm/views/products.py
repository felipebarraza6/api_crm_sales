# DRF
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import (
    IsAuthenticated,
)

# Models
from api.crm.models import Product, Category, Inventory, Price

# Filters
from django_filters import rest_framework as filters

# Serializers
from api.crm.serializers import (ProductModelSerializer,
                                 CategoryModelSerializer,
                                 ProductDetailSerializer,
                                 ListProductsSerializer,
                                 DetailCategorySerializer,
                                 UpdateIventorySerializer,
                                 PriceModelSerializer,
                                 CreatePriceModelSerializer,
                                 UpdateModelSerializer)


# Categories ViewSet
class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):

    queryset = Category.objects.all().order_by("created")
    filter_backends = (filters.DjangoFilterBackend,)
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    class CategoryFilter(filters.FilterSet):
        class Meta:
            model = Category
            fields = {
                'name': ['contains']
            }

    filterset_class = CategoryFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return DetailCategorySerializer
        if self.action == 'retrieve':
            return DetailCategorySerializer
        else:
            return CategoryModelSerializer


# Poducts ViewSet
class ProductViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Product.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    class ProductFilter(filters.FilterSet):
        class Meta:
            model = Product
            fields = {
                'name': ['contains'],
                'category': ['exact'],
            }

    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ListProductsSerializer
        if self.action == 'retrieve':
            return ProductDetailSerializer
        else:
            return ProductModelSerializer


# Inventories ViewSet
class InventoryViewSet(viewsets.GenericViewSet,
                       mixins.UpdateModelMixin):
    queryset = Inventory.objects.all().order_by('-created')
    filter_backends = (filters.DjangoFilterBackend,)
    lookup_field = 'uuid'
    permission_classes = [IsAuthenticated]

    class InventoryFilter(filters.FilterSet):
        class Meta:
            model = Inventory
            fields = {
                'product': ['exact'],
            }

    filterset_class = InventoryFilter
    serializer_class = UpdateIventorySerializer


# Price ViewSet
class PriceViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin):
    queryset = Price.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    class PriceFilter(filters.FilterSet):
        class Meta:
            model = Price
            fields = {
                'title': ['contains'],
                'price': ['contains', 'exact'],
                'is_normal_price': ['exact'],
                'is_delivery': ['exact'],
                'product': ['exact']

            }

    filterset_class = PriceFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return CreatePriceModelSerializer
        if self.action == 'partial_update':
            return UpdateModelSerializer
        else:
            return PriceModelSerializer
