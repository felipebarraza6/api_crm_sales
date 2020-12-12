"""Clients Models."""

#Django
from django.db import models
from django.core.validators import RegexValidator

#Utils
from .utils import ApiModel


class Client(ApiModel):    
    
    #Regex Validator
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="The phone number must be entered in the format: +9999999. Up to 15 digits are allowed."
    )

    #General
    first_name = models.CharField(max_length=40, blank=False, null=False)
    last_name = models.CharField(max_length=60, blank=True, null=True)
    dni = models.CharField('dni', unique=True,max_length=10, null=True, blank=True,
        error_messages={
			'unique' : "Un cliente ya tiene este rut."
		}
    )    
    
    #Contact Info
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False, null=False, unique=True,
        error_messages={
			'unique' : "Un cliente ya tiene este numero de telefono."
		}
    )
    email = models.EmailField(
		'email',
		unique = True,
		error_messages={
			'unique' : "Un cliente(empresa) con ese email ya existe."
		},
		null= True,
		blank = True
	)
    
    #GeoInfo
    region = models.CharField(default="Región de Ñuble", max_length=20)
    province = models.CharField(default="Diguillin", max_length=20)
    commune = models.CharField(default="Chillán", max_length=20)
    address_exact = models.CharField(max_length=60, null=True, blank=True)
    latitud = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    is_active = models.BooleanField(
		'is Active',
		default = True
	)

    
    def __str__(self):
        return str(('{} {}').format(self.first_name, self.last_name))

    def full_name(self):
        return ("{} {}").format(self.first_name, self.last_name)