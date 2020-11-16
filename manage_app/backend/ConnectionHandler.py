import asyncio
import paramiko
import time
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
            hostname=self.device_model.hostname,
            port=22,
            username=self.conf_model.login_username,
            password=self.conf_model.login_password
        )

        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connection.connect(**login_params)
        self.shell_connection = self.connection.invoke_shell()
        self.shell_connection.send('terminal length 0\n')

        logging.warning(f'Successfully opened SSH session with {self.device_model.hostname}:22.')

        return self

    @staticmethod
    async def write_to_connection(self, command_string):
        if self.shell_connection.send_ready():
            self.shell_connection.send(command_string)
            logging.warning(f'Command sent - {command_string}')

    @staticmethod
    async def read_from_connection(self):
        if self.shell_connection.recv_ready():
            return self.shell_connection.recv(5000).decode('utf-8')
