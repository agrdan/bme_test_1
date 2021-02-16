from threading import Thread
from time import sleep
import time
import sched
from mqtt import MqttClient
from controller.BMEController import BMEController, Bme680Dto
from helper import app
from datetime import datetime as dt
from controller.DBInit import DBInit
from controller.bme_680 import BME680
from pathlib import Path
import uuid
from air_quality.MapQuality import MapQuality
from model.AzureBmeDto import AzureBmeDto
from azure.AzureClient import AzureClient
import asyncio

CONNECTION_STRING = "HostName=AirAnalyzerSensors.azure-devices.net;DeviceId=BME680M;SharedAccessKey=b0qBtEZzpgF7tiV7jaWqVRO3slgLeZxW4v7OfFSMp+o="



def initializeProject():
    DBInit()


class DeviceUUID:

    def __init__(self):
        exists = self.check_if_uuid_exists()
        if not exists:
            print("Generating UUID!")
            self.createUUID()

    def check_if_uuid_exists(self):
        uuid_file = Path("uuid.txt")
        if uuid_file.is_file():
            return True
        else:
            return False


    def createUUID(self):
        uuid_file = open("uuid.txt", "w")
        generatedUUID = uuid.uuid4()
        uuid_file.write(str(generatedUUID))
        uuid_file.close()


    def readUUID(self):
        uuid_file = open("uuid.txt", "r")
        uuid = uuid_file.readline()
        uuid_file.close()
        return uuid


class AppMain(Thread):

    global CONNECTION_STRING

    def __init__(self, devId):
        Thread.__init__(self)
        self.bmeController = BME680()
        self.lastTimeSent = None
        self.devId = devId
        print("Main initalized! DeviceUUID[{}]".format(self.devId))

    def run(self):
        self.client = AzureClient(CONNECTION_STRING)
        asyncio.run(self.client.connect())
        while True:
            reading = self.bmeController.read_data()
            send, model = self.send(reading)
            print(model)
            try:
                if send:
                    asyncio.run(self.client.publish(model))
            except Exception as e:
                print(e)
            sleep(5)


    def send(self, dto):
        if self.lastTimeSent is None:
            self.lastTimeSent = dt.now()
            return False, None
        else:
            diff = dt.now() - self.lastTimeSent
            print("Seconds dif: {}".format(diff.seconds))
            if diff.seconds > 1800:
                azureDto = AzureBmeDto()
                azureDto.create(self.devId, dto, MapQuality.mapValue(dto.gas))
                self.lastTimeSent = dt.now()
                return True, azureDto.generateJson()
            else:
                return False, None


if __name__ == '__main__':
    initializeProject()
    devUUID = DeviceUUID()
    devId = devUUID.readUUID()
    main = AppMain(devId)
    main.start()
    app.run(host='0.0.0.0')
