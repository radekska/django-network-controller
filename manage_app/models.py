from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class DeviceModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    device_hostname = models.CharField(max_length=50)
    system_description = models.CharField(max_length=1000, default=None)


class DeviceInterface(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    device_model = models.ForeignKey(DeviceModel, on_delete=models.CASCADE, default=None)

    interface_name = models.CharField(max_length=50)
    interface_bandwidth = models.CharField(max_length=20)
    interface_description = models.CharField(max_length=100)
