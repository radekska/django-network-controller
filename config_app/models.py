from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class ConfigParameters(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    secret = models.CharField(max_length=50)

    network_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)
    subnet = models.IntegerField(validators=(MinValueValidator(0), MaxValueValidator(32)))

    network_device_os = models.CharField(max_length=50)
    discovery_protocol = models.CharField(max_length=50)
