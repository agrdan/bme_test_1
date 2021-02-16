from decimal import Decimal as BigDecimal
import json

class Bme680Dto:

    def __init__(self):

        self.temperature: BigDecimal = None
        self.gas: BigDecimal = None
        self.humidity: BigDecimal = None
        self.pressure: BigDecimal = None

    def setReading(self, temperature, gas, humidity, pressure):
        self.temperature = temperature
        self.gas = gas
        self.humidity = humidity
        self.pressure = pressure


    def fromJson(self, bme):
        parse = json.loads(bme)
        self.temperature = parse['temperature']
        self.gas = parse['gas']
        self.humidity = parse['humidity']
        self.pressure = parse['pressure']

    def getJson(self):
        bme680 = {
            'temperature': self.temperature,
            'gas': self.gas,
            'humidity': self.humidity,
            'pressure': self.pressure
        }

        return json.dumps(bme680)

    def __repr__(self):
        return str(self.__dict__)
