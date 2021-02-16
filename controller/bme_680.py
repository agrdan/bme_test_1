import board
import busio
import adafruit_bme680
from model.Bme680Dto import Bme680Dto


class BME680:

    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_bme680.Adafruit_BME680_I2C(self.i2c)
        print("BME680 I2C initialized!")
        self.read_data()


    def read_data(self):
        bme680 = Bme680Dto()
        bme680.setReading(self.sensor.temperature, self.sensor.gas,
                           self.sensor.humidity, self.sensor.pressure)
        #print(bme680.getJson())

        return bme680





