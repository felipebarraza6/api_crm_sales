# DRF
from rest_framework import serializers

# Models
from api.crm.models import SalesModule, User, Payment

# Serializers
from .orders import OrderModelSerializer


class CreateSalesModuleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SalesModule
        fields = '__all__'

    def validate(self, data):
        list_sales_modules = SalesModule.objects.filter(user=data['user'])
        if data['initial_amount'] < 0:
            raise serializers.ValidationError('Debe ser un numero entero positivo')

        for p in list_sales_modules:
            if p.is_active:
                raise serializers.ValidationError(
                    'Tienes un modulo de ventas activo, debes cerrarlo para crear uno nuevo')
        return data


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email'
        )


class PaymentData(serializers.ModelSerializer):
    type_payment = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = (
            'id',
            'created',
            'type_payment',
            'amount_final',
            'order'
        )


class ListSalesModuleSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()

    class Meta:
        model = SalesModule
        fields = '__all__'


class RetrieveModuleSales(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField('get_payments')
    user = UserModelSerializer()
    cash = serializers.SerializerMethodField('get_cash')
    debit_card = serializers.SerializerMethodField('get_debit_card')
    credit_card = serializers.SerializerMethodField('get_credit_card')
    agreement = serializers.SerializerMethodField('get_agreement')

    def get_payments(self, module):
        qs = Payment.objects.filter(sales_module=module)
        serializer = PaymentData(instance=qs, many=True)
        return serializer.data

    def get_debit_card(self, module):
        qs = Payment.objects.filter(sales_module=module, type_payment__is_debit_card=True)
        serializer = PaymentData(instance=qs, many=True)
        return serializer.data

    def get_credit_card(self, module):
        qs = Payment.objects.filter(sales_module=module, type_payment__is_credit_card=True)
        serializer = PaymentData(instance=qs, many=True)
        return serializer.data

    def get_agreement(self, module):
        qs = Payment.objects.filter(sales_module=module, type_payment__is_agreement=True)
        serializer = PaymentData(instance=qs, many=True)
        return serializer.data

    def get_cash(self, module):
        qs = Payment.objects.filter(sales_module=module, type_payment__is_cash=True)
        serializer = PaymentData(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = SalesModule
        fields = (
            'id',
            'created',
            'user',
            'initial_amount',
            'finish_amount',
            'quantity_orders',
            'date_finish',
            'is_active',
            'payments',
            'cash',
            'debit_card',
            'credit_card',
            'agreement',
        )


class RetrieveModuleSalesInRetrieveUser(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField('get_payments')

    def get_payments(self, module):
        qs = Payment.objects.filter(sales_module=module)
        serializer = PaymentData(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = SalesModule
        fields = (
            'id',
            'created',
            'date_finish',
            'initial_amount',
            'quantity_orders',
            'finish_amount',
            'is_active',
            'payments'
        )


class FinishModuleSales(serializers.ModelSerializer):
    date_finish = serializers.DateTimeField()

    class Meta:
        model = SalesModule
        fields = ('is_active', 'date_finish', 'id')

    def validate(self, data):
        user_module = self.instance.user
        user_request = self.context['request'].user
        is_active_old = self.instance.is_active
        if user_module != user_request:
            raise serializers.ValidationError('Solo el propietario del modulo puede cerrarlo')
        elif is_active_old is False:
            raise serializers.ValidationError('El modulo de ventas cerrado ya fue cerrado')
        return data

