from decimal import Decimal as BigDecimal
import json

class ExportBMEDto:
    def __init__(self):

        self.temperature: BigDecimal = None
        self.gas: BigDecimal = None
        self.humidity: BigDecimal = None
        self.pressure: BigDecimal = None
        self.time: str = None

    def __repr__(self):
        return str(self.__dict__)