from datetime import datetime as dt
from model.Bme680Dto import Bme680Dto
import json

class AzureBmeDto:

    def __init__(self):
        self.uuid: str = None
        self.temperature: float = None
        self.humidity: float = None
        self.pressure: float = None
        self.iaq: int = None
        self.quality: str = None
        self.created = str(int(dt.now().timestamp()))


    def create(self, uuid, dto: Bme680Dto, quality):
        self.uuid = uuid
        self.temperature = dto.temperature
        self.humidity = dto.humidity
        self.pressure = dto.pressure
        self.iaq = dto.gas
        self.quality = quality


    def generateJson(self):
        azureJson = {
            'Uuid': self.uuid,
            'Temperature': self.temperature,
            'Humidity': self.humidity,
            'Air pressure': self.pressure,
            'Air quality': {
                'value': self.iaq,
                'quality': self.quality
            }
        }
        return json.dumps(azureJson)


"""
{
Uuid,
Temperature : float,
Humidity: float,
Air pressure: float,
Air quality : payload (tu bi kao trebali oni plinovi pa na svaki float za postotak),
TimeCreated
}
"""