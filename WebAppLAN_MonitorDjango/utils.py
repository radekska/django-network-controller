from config_app.models import AvailableDevices


def get_available_devices():
    return [host.network_address for host in AvailableDevices.objects.all()]
