import logging
import asyncio
import json
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from manage_app.backend.ConnectionHandler import SSHConnectionHandler

from config_app.models import ConfigParameters
from manage_app.models import DeviceModel


class SSHConsumer(AsyncConsumer):
    socket_opened = False

    async def websocket_connect(self, event):
        logging.warning(f"Web socket opened - {event}.")
        await self.send({
            'type': 'websocket.accept',
        })

        self.device_model = await sync_to_async(DeviceModel.objects.get, thread_sensitive=True)(ssh_session=True)
        self.device_id = self.device_model.id

        self.access_config_model = await sync_to_async(ConfigParameters.objects.get, thread_sensitive=True)(
            access_config_id__isnull=False)
        self.access_config_id = self.access_config_model.access_config_id

        await self.send({
            'type': 'websocket.send',
            'text': f'\r\nOpening SSH session to {self.device_model.hostname}... \r\n'
        })

        self.SSHConnection = await SSHConnectionHandler.initialize_connection(self.device_id, self.access_config_id)
        initial_response = await self.SSHConnection.read_from_connection(self.SSHConnection)
        await asyncio.sleep(1)

        await self.send({
            'type': 'websocket.send',
            'text': initial_response
        })

    async def websocket_receive(self, event):
        command = event.get('text', None)

        responded_lines, response = await asyncio.gather(
            self.SSHConnection.write_to_connection(self.SSHConnection, command),
            self.SSHConnection.read_from_connection(self.SSHConnection))

        if response is not False:
            await self.send({
                'type': 'websocket.send',
                'text': response
            })

    async def websocket_disconnect(self, event):
        self.device_model.ssh_session = False
        await sync_to_async(self.device_model.save, thread_sensitive=True)()
        logging.warning("connection closed", event)
