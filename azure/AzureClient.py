from time import sleep as delay
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from datetime import datetime as dt
from threading import Thread
from collections import deque


class AzureClient:

    def __init__(self, connectionString):
        self.connectionString = connectionString
        self.queue = deque()

    async def connect(self):
        deviceClient = IoTHubDeviceClient.create_from_connection_string(self.connectionString)
        await deviceClient.connect()
        self.device = deviceClient
        self.device.on_message_received = self.azureMessageCallback

    def getClient(self):
        return self.device

    async def disconnect(self, client):
        if client.connected:
            await client.disconnect()

    async def publish(self, msg):
        if self.device.connected:
            print("Trying to publish message...\n{}".format(msg))
            await self.device.send_message(msg)
            print("Message sent!")
        else:
            print("Client not connected")

    def azureMessageCallback(self, message):
        print("Message received [{}]".format(dt.now()))
        print(message.data)
        print(message.custom_properties)
        self.queue.append(str(message.data, 'utf-8'))

    def getFromQueue(self):
        if len(self.queue) is not 0:
            return self.queue.popleft()
        else:
            return None