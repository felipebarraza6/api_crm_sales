"""Payment Serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from api.crm.models import Payment, TypePayment, Delivery, Order


class TypePaymentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypePayment
        fields = '__all__'


class UpdateTypePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypePayment
        fields = (
            'name',
            'description',
            'tax_porcent',
            'tax_static_value'
        )

    def update(self, instance, validated_data):
        if instance.is_tax_porcent:
            if 'tax_static_value' in validated_data:
                raise serializers.ValidationError('Este impuesto no corresponde a este tipo de pago')
        elif instance.is_tax_static_value:
            if 'tax_porcent' in validated_data:
                raise serializers.ValidationError('Este impuesto no corresponde a este tipo de pago')

        return instance


class CreateTypePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypePayment
        fields = (
            'name',
            'description',
            'is_tax_porcent',
            'tax_porcent',
            'is_tax_static_value',
            'tax_static_value',
            'is_cash',
            'is_credit_card',
            'is_debit_card',
            'is_agreement'
        )

    def validate(self, data):
        if 'is_tax_porcent' not in data and 'is_tax_static_value' not in data:
            raise serializers.ValidationError('Debes elegir al menos un tipo de impuesto')

        elif 'is_tax_porcent' in data and 'is_tax_static_value' in data:
            raise serializers.ValidationError('Debes elegir una opcion de impuestos no ambas')

        if 'is_tax_porcent' in data:
            if 'tax_porcent' not in data:
                raise serializers.ValidationError('Debes establecer el valor de impuesto en porcentaje')
        elif 'is_tax_static_value' in data:
            if 'tax_static_value' not in data:
                raise serializers.ValidationError('Debes establecer el valor de impuesto en un monto estatico')

        if 'is_cash' not in data and \
                'is_credit_card' not in data and \
                'is_debit_card' not in data and \
                'is_agreement' not in data:
            raise serializers.ValidationError(
                'Debes seleccionar el tipo de medio de pago; efectivo, tarjeta de credito, tarjeta de debito o convenio'
            )

        return data


class PaymentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class CreatePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'order',
            'sales_module',
            'amount_pay',
            'type_payment'
        )

    def validate(self, data):

        if 'type_payment' not in data:
            raise serializers.ValidationError(
                'Debes ingresar el tipo de pago'
            )

        elif not data['sales_module'].is_active:
            raise serializers.ValidationError(
                'Modulo de ventas cerrado, debes re abrirlo o crear un modulo de ventas nuevo'
            )

        elif data['order'].is_paid:
            raise serializers.ValidationError('El pedido está pagado')

        elif not data['order'].is_active:
            raise serializers.ValidationError('El pedido no esta activo')

        calculate_porcent_with_type_payment = 0

        if data['type_payment'].is_tax_porcent:
            calculate_porcent_with_type_payment = (data['order'].total_with_taxts * data['type_payment'].tax_porcent) + \
                                                  data['order'].total_with_taxts
        elif data['type_payment'].is_tax_static_value:
            calculate_porcent_with_type_payment = data['order'].total_with_taxts + data['type_payment'].tax_static_value

        if data['amount_pay'] < calculate_porcent_with_type_payment:
            raise serializers.ValidationError(
                'El monto a pagar debe ser mayor o igual a {}'.format(calculate_porcent_with_type_payment))
        elif data['amount_pay'] > calculate_porcent_with_type_payment:
            change_for_pay =  data['amount_pay'] - calculate_porcent_with_type_payment
            data['amount_change'] = change_for_pay

        data['amount_final'] = calculate_porcent_with_type_payment

        return data
