# DRF
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

# Models
from api.crm.models import Payment, TypePayment

# Filters
from django_filters import rest_framework as filters

# Serializers
from api.crm.serializers import (PaymentModelSerializer,
                                 CreatePaymentSerializer,
                                 TypePaymentModelSerializer,
                                 CreateTypePaymentSerializer,
                                 UpdateTypePaymentSerializer)


# TypePayment Views
class TypePayment(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin):

    queryset = TypePayment.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    class TypePaymentFilter(filters.FilterSet):
        class Meta:
            model = TypePayment
            fields = {
                'name': ['contains', 'exact'],
                'is_tax_porcent': ['exact'],
                'is_tax_static_value': ['exact'],
                'is_cash': ['exact'],
                'is_credit_card': ['exact'],
                'is_debit_card': ['exact'],
                'is_agreement': ['exact']
            }

    filterset_class = TypePaymentFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTypePaymentSerializer
        elif self.action == 'list':
            return TypePaymentModelSerializer
        elif self.action == 'partial_update':
            return UpdateTypePaymentSerializer


# Payment Views
class PaymentOrder(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin):
    queryset = Payment.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    lookup_field = 'id'

    permission_classes = [IsAuthenticated]

    class PaymentFilter(filters.FilterSet):
        class Meta:
            model = Payment
            fields = {
                'type_payment': ['exact'],
                'type_payment__is_cash': ['exact'],
                'sales_module': ['exact'],
                'order': ['exact'],
                'created': [
                    'contains',
                    'gte',
                    'lte',
                    'year',
                    'month',
                    'day',
                    'year__range',
                    'month__range',
                    'day__range',
                    'date__range'
                ],
            }

    filterset_class = PaymentFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'destroy':
            return PaymentModelSerializer

        if self.action == 'create':
            return CreatePaymentSerializer
