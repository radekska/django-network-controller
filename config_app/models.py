from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class ConfigParameters(models.Model):
    """
    This class inherits built-in models.Model class from django.db package and with it's help creates
    a table in specified database with below parameters:
    - user
    - login_username
    - login_password
    - network_ip
    - network_device_os
    - secret
    - subnet_cidr
    - snmp_config_id
    - access_config_id
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)

    login_username = models.CharField(max_length=50)
    login_password = models.CharField(max_length=50)

    network_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)
    network_device_os = models.CharField(max_length=50)

    secret = models.CharField(max_length=50)
    subnet_cidr = models.IntegerField(validators=(MinValueValidator(0), MaxValueValidator(32)))

    snmp_config_id = models.IntegerField(default=None, null=True)
    access_config_id = models.IntegerField(default=None, null=True)


class AvailableDevices(models.Model):
    """
    This class inherits built-in models.Model class from django.db package and with it's help creates
    a table in specified database with below parameters:
    - user
    - network_address
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    network_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)


class SNMPConfigParameters(models.Model):
    """
    This class inherits built-in models.Model class from django.db package and with it's help creates
    a table in specified database with below parameters:
    ### Obligatory ###
    - user
    - group_name
    - snmp_user
    - snmp_password
    - snmp_auth_protocol
    - snmp_privacy_protocol
    - snmp_encrypt_key
    - snmp_host
    ### Optional ###
    - server_location
    - contact_details
    - enable_traps
    - traps_activated (required if traps enabled)
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)

    group_name = models.CharField(max_length=50)
    snmp_user = models.CharField(max_length=50)
    snmp_password = models.CharField(max_length=50)
    snmp_auth_protocol = models.CharField(max_length=10, default=None, null=True)
    snmp_privacy_protocol = models.CharField(max_length=10, default=None, null=True)
    snmp_encrypt_key = models.CharField(max_length=50)
    snmp_host = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)

    server_location = models.CharField(max_length=50, default=None, null=True, blank=True)
    contact_details = models.EmailField(max_length=50, default=None, null=True, blank=True)
    enable_traps = models.BooleanField(null=True, blank=True)
    traps_activated = models.BooleanField(default=False, null=True, blank=True)
