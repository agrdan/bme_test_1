import board
import busio
import adafruit_bme680
from model.Bme680Dto import Bme680Dto


class BME680:

    # konstruktor klase koja koristi library adafruid za citanje podatke s registra senzora
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA) # konstruktor I2C modula
        self.sensor = adafruit_bme680.Adafruit_BME680_I2C(self.i2c) # konstruktor senzora (preko I2C-a iznad)
        print("BME680 I2C initialized!")
        self.read_data()


    # library cita podatke s registra senzora, a mi s ovom metodom samo filamo DTO preko vrijednosti koje procitamo s "sensor" objekta i vracamo dto
    def read_data(self):
        bme680 = Bme680Dto()
        bme680.setReading(self.sensor.temperature, self.sensor.gas,
                           self.sensor.humidity, self.sensor.pressure)
        #print(bme680.getJson())

        return bme680





