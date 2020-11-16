import logging
import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from manage_app.backend.ConnectionHandler import SSHConnectionHandler


class SSHConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        logging.warning(f"Web socket opened - {event}.")
        await self.send({
            'type': 'websocket.accept',
        })

        await self.send({
            'type': 'websocket.send',
            'text': 'Opening SSH session to <host>... \r\n'
        })

        self.SSHConnection = await SSHConnectionHandler.initialize_connection(45, 1)
        await asyncio.sleep(1)

        initial_response = await self.SSHConnection.read_from_connection(self.SSHConnection)
        await self.send({
            'type': 'websocket.send',
            'text': initial_response
        })

    async def websocket_receive(self, event):
        command = event.get('text', None)
        await self.SSHConnection.write_to_connection(self.SSHConnection, command)

        response = await self.SSHConnection.read_from_connection(self.SSHConnection)
        await self.send({
            'type': 'websocket.send',
            'text': response
        })

    async def websocket_disconnect(self, event):
        logging.warning("connection closed", event)
