import netmiko
import logging
from asgiref.sync import sync_to_async
from manage_app.models import DeviceModel
from config_app.models import ConfigParameters


class SSHConnectionHandler:

    @classmethod
    async def initialize_connection(cls, device_id, conf_access_id):
        self = SSHConnectionHandler()
        self.device_model = await sync_to_async(DeviceModel.objects.get, thread_sensitive=True)(id=device_id)
        self.conf_model = await sync_to_async(ConfigParameters.objects.get, thread_sensitive=True)(id=conf_access_id)

        login_params = dict(
            ip=self.device_model.hostname,
            username=self.conf_model.login_username,
            password=self.conf_model.login_password,
            secret=self.conf_model.login_password
        )

        try:
            self.connection = netmiko.BaseConnection(**login_params)
            self.connection.set_terminal_width('511')
            self.connection.write_channel('terminal length 0\n')

            logging.warning(f'Successfully opened SSH session with {self.device_model.hostname}:22.')

            return self
        except Exception as e:
            logging.warning(e)

    @staticmethod
    async def write_to_connection(self, command_string):
        logging.warning(f'Command sent - {command_string}')
        self.connection.write_channel(command_string)

    @staticmethod
    async def read_from_connection(self):
        try:
            response = self.connection.read_until_prompt()
            current_prompt = self.connection.find_prompt()
            response_in_lines = response.split('\n')
            response_in_lines.pop(0)

            response = '\n' + '\n'.join(response_in_lines)
            data = dict(response=response, current_prompt=current_prompt)

            return data
        except Exception as e:
            logging.warning(e)
            return False
