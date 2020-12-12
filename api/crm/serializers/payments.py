"""Payment Serializers."""

#Django REST Framework
from rest_framework import serializers


#Models
from api.crm.models import Payment, TypePayment, Delivery, Order


class TypePaymentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypePayment
        fields = '__all__'

class PaymentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model= Payment
        fields= '__all__'


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
        if data['sales_module'].is_active == False:
            raise serializers.ValidationError('Modulo de ventas cerrado, debes re abrirlo o crear un modulo de ventas nuevo')
        if data['order'].is_paid == True:
            raise serializers.ValidationError('El pedido está pagado')

        if data['order'].is_active == False:
            raise serializers.ValidationError('El pedido esta anulado')
        
        order_total_amount = data['order'].total_amount

        tax_value = 0

        if data['order'].is_delivery == True:                        
            get_deli_service = Delivery.objects.filter(id=data['order'].delivery.id).first()            
            if get_deli_service.is_tax_porcent == True:
                tax_value = (order_total_amount * get_deli_service.tax_porcent)
            elif get_deli_service.is_tax_static_value == True:
                tax_value =  get_deli_service.tax_static_value

        operation_calculate = 0

        if data['type_payment'].is_tax_porcent:
            operation_calculate = (order_total_amount * data['type_payment'].tax_porcent)
        elif data['type_payment'].is_tax_static_value:
            operation_calculate = data['type_payment'].tax_static_value
        
        with_taxts = int(order_total_amount + operation_calculate + tax_value)
        
        Order.objects.filter(id=data['order'].id).update(
                total_with_taxts = with_taxts
        )

        if data['amount_pay'] < with_taxts:
            raise serializers.ValidationError('El monto a pagar deber ser igual o mayor al total de {}'.format(with_taxts))

        

        return data
