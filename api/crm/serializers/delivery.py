"""Deliveries Serializers."""

#DRF
from rest_framework import serializers

#Models
from api.crm.models import Delivery


class DeliveriesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'

    def validate(self, data):        
        if 'is_tax_porcent' in data:
            is_porcent = data['is_tax_porcent']                        
            if is_porcent == True:
                if 'tax_porcent' not in data:
                    raise serializers.ValidationError('Debes ingresar el porcentaje')
        if 'is_tax_static_value' in data:
            is_static_value = data['is_tax_static_value']
            if is_static_value == True:
                if 'tax_static_value':
                    raise serializers.ValidationError('Debes ingresar el valor')

        return data

class DeliveriesForProductRetrieve(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = (
            'id',
            'name_service'
        )