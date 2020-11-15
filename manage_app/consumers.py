import logging
import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async


class SSHConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        logging.warning(f"Web socket opened - {event}")
        await self.send({
            'type': 'websocket.accept',
        })

        await self.send({
            'type': 'websocket.send',
            'text': 'Opening SSH session to <host>... \r\n'
        })

    async def websocket_receive(self, event):
        print("received message", event)

    async def websocket_disconnect(self, event):
        print("connection closed", event)
