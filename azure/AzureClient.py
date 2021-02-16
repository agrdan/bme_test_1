from time import sleep as delay
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from datetime import datetime as dt
from threading import Thread
from collections import deque


class AzureClient:

    def __init__(self, connectionString): # konstruktor azure klienta
        self.connectionString = connectionString # string s kojim se identificiramo kao BME680 senzor
        self.queue = deque() #queue pripremljen za poruke kad je senzor u sleepu

    async def connect(self):
        deviceClient = IoTHubDeviceClient.create_from_connection_string(self.connectionString) # iz librarya konstruktor
        await deviceClient.connect() # await -> ceka do kad se klijent ne spoji na azure
        self.device = deviceClient # device klijent spremimo u varijablu da se moze koristiti u cijeloj klasi
        self.device.on_message_received = self.azureMessageCallback # callback metoda izjednacena s onom iz libraria (kad prime oni poruku, primimo i mi u svojoj)

    def getClient(self):
        return self.device

    async def disconnect(self, client):
        if client.connected:
            await client.disconnect()

    # metoda za publish poruke prema azure-u
    async def publish(self, msg):
        if self.device.connected: # provjera da li spojen
            print("Trying to publish message...\n{}".format(msg))
            await self.device.send_message(msg) # publisha se poruka i ceka se do kad ne zavrsi
            print("Message sent!")
        else:
            print("Client not connected")

    # callback metoda koja cita poruke s azure-a i puni queue
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