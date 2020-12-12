"""Configs Serializers."""

#DRF
from rest_framework import serializers

#Models 
from api.crm.models import Config


class ConfigModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = (
            'name_enterprise',
            'logo',
            'description',
            'exact_address'
        )