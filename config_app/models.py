from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class ConfigParameters(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)

    login_username = models.CharField(max_length=50)
    login_password = models.CharField(max_length=50)
    secret = models.CharField(max_length=50)

    network_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)
    subnet_cidr = models.IntegerField(validators=(MinValueValidator(0), MaxValueValidator(32)))

    network_device_os = models.CharField(max_length=50)
    discovery_protocol = models.CharField(max_length=50)


class AvailableDevices(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    network_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)


class SNMPConfigParameters(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)

    # obligatory parameters
    group_name = models.CharField(max_length=50)
    snmp_user = models.CharField(max_length=50)
    snmp_password = models.CharField(max_length=50)
    snmp_encrypt_key = models.CharField(max_length=50)
    snmp_host = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)

    # additional not obligatory parameters
    server_location = models.CharField(max_length=50, default=None, null=True, blank=True)
    contact_details = models.EmailField(max_length=50, default=None, null=True, blank=True)
    enable_traps = models.BooleanField(null=True, blank=True)  # checkbox
