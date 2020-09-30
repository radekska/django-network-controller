from config_app.models import ConfigParameters
from config_app.backend.static import device_os


def parse_config(object_id):
    config = {
        "user": {
            "username": None,
            "password": None,
            "secret": None,
        },
        "ip_range": {
            "network_ip": None,
            "subnet": None
        },
        "system": {
            "network_dev_os": None,
            "discovery_proto": None

        }
    }

    config_obj = ConfigParameters.objects.filter(id=object_id)[0]

    config["user"]["username"] = config_obj.login_username
    config["user"]["password"] = config_obj.login_password
    config["user"]["secret"] = config_obj.secret

    config["ip_range"]["network_ip"] = config_obj.network_ip
    config["ip_range"]["subnet"] = config_obj.subnet_cidr

    config["system"]["network_dev_os"] = device_os.get(config_obj.network_device_os , 'cisco_ios')
    config["system"]["discovery_proto"] = config_obj.discovery_protocol

    login_params_napalm = {'username': config['user'].get('username'), 'password': config['user'].get('password'),
                           'optional_args': {'secret': config['user'].get('secret')}}

    login_params_netmiko = {'username': config['user'].get('username'), 'password': config['user'].get('password'),
                            'secret': config['user'].get('secret'),
                            'device_type': config['system'].get('network_dev_os')

                            }

    login_params = {'netmiko': login_params_netmiko, 'napalm': login_params_napalm}

    return config, login_params
