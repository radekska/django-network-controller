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
    full_system_name = models.CharField(max_length=50, default=None, null=True)
    system_name = models.CharField(max_length=50, default=None, null=True)
    system_location = models.CharField(max_length=50, default=None)
    system_up_time = models.CharField(max_length=100, default=None, null=True)
    if_number = models.IntegerField(default=None, null=True)
    device_type = models.CharField(max_length=10, default=None, null=True)


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

    interface_in_unicast_packets = models.CharField(max_length=50, default=None, null=True)
    interface_in_errors = models.CharField(max_length=20, default=None, null=True)
    interface_out_unicast_packets = models.CharField(max_length=50, default=None, null=True)
    interface_out_errors = models.CharField(max_length=20, default=None, null=True)

    lldp_neighbor_hostname = models.CharField(max_length=50, default=None, null=True)
    lldp_neighbor_interface = models.CharField(max_length=30, default=None, null=True)


class DeviceTrapModel(models.Model):
    device_model = models.ForeignKey(DeviceModel, on_delete=models.CASCADE, default=None)

    trap_date = models.CharField(max_length=50, default=None, null=True)

    trap_domain = models.CharField(max_length=50, default=None, null=True)
    trap_address = models.CharField(max_length=30, default=None, null=True)
    trap_enterprise = models.CharField(max_length=30, default=None, null=True)
    trap_agent_address = models.CharField(max_length=30, default=None, null=True)
    trap_generic = models.CharField(max_length=30, default=None, null=True)
    trap_uptime = models.CharField(max_length=30, default=None, null=True)

    trap_string_data = models.CharField(max_length=200, default=None, null=True)


class VarBindModel(models.Model):
    trap_model = models.ForeignKey(DeviceTrapModel, on_delete=models.CASCADE, default=None)
    trap_oid = models.CharField(max_length=30, default=None, null=True)
    trap_data = models.CharField(max_length=200, default=None, null=True)
