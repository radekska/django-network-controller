import logging
from config_app.models import ConfigParameters, SNMPConfigParameters


def check_initial_configurations_applied():
    """
    This function validates if access/initial configuration and snmp configurations have been applied by the user.
    """
    initial_configurations_done = False
    try:
        _ = ConfigParameters.objects.get(snmp_config_id__isnull=False).snmp_config_id
        initial_configurations_done = True
    except Exception as exception:
        logging.warning(exception)
    finally:
        return initial_configurations_done


def check_if_properly_configured():
    """
    This function checks if access/initial configuration and snmp configurations have been added as well as applied
    by the user.
    Those configurations are the key for whole further backend logic.
    """
    if ConfigParameters.objects.count() == 0 and SNMPConfigParameters.objects.count() == 0:
        context = dict(
            initial_configurations=False,
            initial_configurations_applied=False
        )

    elif not check_initial_configurations_applied():
        context = dict(
            initial_configurations=True,
            initial_configurations_applied=False
        )
    else:
        context = dict(
            initial_configurations=True,
            initial_configurations_applied=True
        )

    return context
