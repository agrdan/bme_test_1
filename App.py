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


# connection string s azure-a
CONNECTION_STRING = "HostName=AirAnalyzerSensors.azure-devices.net;DeviceId=BME680M;SharedAccessKey=b0qBtEZzpgF7tiV7jaWqVRO3slgLeZxW4v7OfFSMp+o="


def initializeProject():
    DBInit()

# klasa za kreiranje unique uuid-a
class DeviceUUID:

    # konstruktor klase
    def __init__(self):
        # provjera da li file koji sadrzi uuid (uuix.txt) postoji
        exists = self.check_if_uuid_exists()
        if not exists: # ako ne postoji
            print("Generating UUID!")
            self.createUUID() # -> kreiraj

    # metoda za provjeru da li file postoji na lokaciji
    def check_if_uuid_exists(self):
        uuid_file = Path("uuid.txt")
        if uuid_file.is_file():
            return True
        else:
            return False

    # metoda kreiraj uuid
    def createUUID(self):
        uuid_file = open("uuid.txt", "w") # -> otvori (i/ili kreiraj file uuid.txt) sa opcijom "w" (write)
        generatedUUID = uuid.uuid4() # sa python library-om uuid kreira se uuid
        uuid_file.write(str(generatedUUID)) # i spremi u file
        uuid_file.close()


    def readUUID(self):
        uuid_file = open("uuid.txt", "r") # -> otvori file s opcijom "r" (read)
        uuid = uuid_file.readline() # procitaj redak s file-a
        uuid_file.close()
        return uuid


class AppMain(Thread): # klasa nasljeduje Thread klasu (overridamo run() -> treba postojati)

    global CONNECTION_STRING

    def __init__(self, devId):
        Thread.__init__(self) # konstruktor nasljedene klase (super() u drugim programskim jezicima)
        self.bmeController = BME680() # konstruktor klase/objekt za bme (cita pomocu adafuit librarya s neta podatke s senzora preko I2C komunikacije)
        self.lastTimeSent = None # kontrolna varijabla za slanje
        self.devId = devId # uuid preuzet u klasi AppMain (da se moze koristiti u svim lokalnim metodama klase)
        print("Main initalized! DeviceUUID[{}]".format(self.devId)) # debug da se Thread startao

    def run(self):
        self.client = AzureClient(CONNECTION_STRING) # instanciranje azure klijenta
        asyncio.run(self.client.connect()) # asyncio -> high level thread -> asinkrono konektira client na azure
        while True: # beskonacna petlja
            reading = self.bmeController.read_data() # iz bme kontrolera procitamo (t,h,p,g vrijednosti) i spremimo u Bme680Dto (reading)
            send, model = self.send(reading) # u metodi send se prosljedi Bme680Dto i provjerava vrijeme te postavlja flag za slanje
            print(model)
            try:
                if send:
                    asyncio.run(self.client.publish(model))
            except Exception as e:
                print(e)
            sleep(5)


    def send(self, dto):
        if self.lastTimeSent is None: # prvi put izvrsena petlja -> vrijednost je None i zapisuje se trenutno vrijeme
            self.lastTimeSent = dt.now()
            return False, None # vracamo 2 propertya [true/false i model] -> prvi je kontrolni flag, drugi je model
        else:
            diff = dt.now() - self.lastTimeSent # provjeravamo razliku proteklu od zapisanog vremena
            print("Seconds dif: {}".format(diff.seconds))
            if diff.seconds > 1800: # ako je razlika veca od X sekundi
                azureDto = AzureBmeDto() # kreiramo objekt pripremljen za azure i Vrbu
                azureDto.create(self.devId, dto, MapQuality.mapValue(dto.gas)) # popunimo vrijednosti (uuid, BmeDto(gas, press, hum i temper), mapper (iz gas vrijednosti u string "bad", "avg" ili "good")
                self.lastTimeSent = dt.now() # spremimo trenutnu vrijednost u kontrolnu
                return True, azureDto.generateJson() # vratimo flag True (spremno za slanje) i model koji šaljemo
            else:
                return False, None

# kreces od maina
if __name__ == '__main__':
    initializeProject() # gore metoda -> iz controller.DBInit() sluzi da se kreira baza iz model.BmeEntity
    devUUID = DeviceUUID() # konstruktor klase -> objekt za citanje uuida -> kreira uuid.txt ako ne postoji, ako postoji ignorira
    devId = devUUID.readUUID() # procita uuid iz file-a
    main = AppMain(devId) # konstruktor klase glavnog threada -> prosljedujemo mu uuid
    main.start() # startamo thread -> prebacujemo se u AppMain klasu
    app.run(host='0.0.0.0')
