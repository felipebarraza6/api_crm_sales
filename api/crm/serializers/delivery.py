"""Deliveries Serializers."""

# DRF
from rest_framework import serializers

# Models
from api.crm.models import Delivery


class UpdateDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = (
            'name_service',
            'description',
            'is_tax_porcent',
            'tax_porcent',
            'is_tax_static_value',
            'tax_static_value',
        )
        read_only_fields = {
            'is_tax_porcent',
            'is_tax_static_value',
        }

    def update(self, instance, validated_data):

        for item in validated_data:
            if Delivery._meta.get_field(item):
                setattr(instance, item, validated_data[item])

        if instance.is_tax_porcent and 'tax_static_value' in validated_data:
            raise serializers.ValidationError('Seleccionaste impuesto por porcentaje debes llenar el campo corecto')

        if instance.is_tax_static_value and 'tax_porcent' in validated_data:
            raise serializers.ValidationError(
                'Seleccionaste impuesto por un valor estatitico, debes llenar el campo corecto')

        instance.save()

        return instance


class CreateDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'

    def validate(self, data):

        if 'is_tax_porcent' in data and 'is_tax_static_value' in data:
            raise serializers.ValidationError('Debes elegir un tipo de impuesto')

        if 'is_tax_porcent' in data:
            is_porcent = data['is_tax_porcent']
            if is_porcent:
                if 'tax_porcent' not in data:
                    raise serializers.ValidationError('Debes ingresar el porcentaje')

        if 'is_tax_static_value' in data:
            is_static_value = data['is_tax_static_value']
            if is_static_value:
                if 'tax_static_value':
                    raise serializers.ValidationError('Debes ingresar el valor')

        return data


class DeliveriesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'


class DeliveriesForProductRetrieve(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = (
            'id',
            'name_service'
        )
