from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class DeviceModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    system_description = models.CharField(max_length=1000, default=None)
    system_version = models.CharField(max_length=50, default=None, null=True)
    system_image = models.CharField(max_length=50, default=None, null=True)
    system_type = models.CharField(max_length=50, default=None, null=True)
    system_contact = models.CharField(max_length=50, default=None)
    system_name = models.CharField(max_length=50, default=None)
    system_location = models.CharField(max_length=50, default=None)
    system_up_time = models.CharField(max_length=100, default=None, null=True)
    if_number = models.IntegerField(default=None, null=True)


class DeviceInterface(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    device_model = models.ForeignKey(DeviceModel, on_delete=models.CASCADE, default=None)

    interface_name = models.CharField(max_length=50, default=None)
    interface_description = models.CharField(max_length=100, default=None)
    interface_mtu = models.CharField(max_length=20, default=None)
    interface_speed = models.CharField(max_length=20, default=None)
    interface_physical_addr = models.CharField(max_length=50, default=None)
    interface_admin_status = models.CharField(max_length=10, default=None)
    interface_operational_status = models.CharField(max_length=10, default=None)
    interface_ip = models.CharField(max_length=50, default=None, null=True)
