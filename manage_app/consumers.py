import json
import logging
import asyncio

from django.contrib.auth.models import User

from asgiref.sync import sync_to_async
from channels.consumer import AsyncConsumer

from manage_app.backend.ConnectionHandler import SSHConnectionHandler

from config_app.models import ConfigParameters
from manage_app.models import DeviceModel


class SSHConsumer(AsyncConsumer):
    """
    This class is inherits from AsyncConsumer class from channels.consumer module and it is responsible for handling all
    asynchronous traffic coming from javascript frontend web socket as well as forwarding it further to Network Device. (xterm SSH web terminal)
    """
    socket_opened = False

    async def websocket_connect(self, event):
        self.user = self.scope["user"]

        logging.warning(f"Web socket opened - {event}.")
        await self.send({
            'type': 'websocket.accept',
        })

        self.device_model = await sync_to_async(DeviceModel.objects.get, thread_sensitive=True)(ssh_session=True)
        self.device_id = self.device_model.id

        self.user_model = await sync_to_async(User.objects.get, thread_sensitive=True)(
            username=self.user)
        self.access_config_model = await sync_to_async(ConfigParameters.objects.filter, thread_sensitive=True)(
            access_config_id__isnull=False)
        self.access_config_model = await sync_to_async(self.access_config_model.get, thread_sensitive=True)(
            user=self.user_model)
        self.access_config_id = self.access_config_model.access_config_id

        initial_data = dict(response=f'\r\nOpening SSH session to {self.device_model.hostname}... \r\n')

        await self.send({
            'type': 'websocket.send',
            'text': json.dumps(initial_data)
        })

        self.SSHConnection = await SSHConnectionHandler.initialize_connection(self.device_id, self.access_config_id)
        data = await self.SSHConnection.read_from_connection(self.SSHConnection)
        await asyncio.sleep(1)

        await self.send({
            'type': 'websocket.send',
            'text': json.dumps(data),

        })

    async def websocket_receive(self, event):
        command = event.get('text', None)

        responded_lines, response_and_prompt = await asyncio.gather(
            self.SSHConnection.write_to_connection(self.SSHConnection, command),
            self.SSHConnection.read_from_connection(self.SSHConnection))

        if response_and_prompt is not False:
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps(response_and_prompt)
            })

    async def websocket_disconnect(self, event):
        self.device_model.ssh_session = False
        await sync_to_async(self.device_model.save, thread_sensitive=True)()
        logging.warning("connection closed", event)
