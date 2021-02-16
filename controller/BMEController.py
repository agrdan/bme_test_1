from model.Bme680Dto import Bme680Dto
from model.BmeEntity import BmeEntity
from model.ExportBMEDto import ExportBMEDto
from helper import db
from datetime import datetime as dt


class BMEController:

    @staticmethod
    def dtoToEntity(dto: Bme680Dto):
        e = BmeEntity()
        e.temperature = dto.temperature
        e.gas = dto.gas
        e.humidity = dto.humidity
        e.pressure = dto.pressure
        e.time = str(dt.now())
        return e

    @staticmethod
    def entityToDto(entity: BmeEntity):
        dto = Bme680Dto()
        dto.temperature = entity.temperature
        dto.gas = entity.gas
        dto.humidity = entity.humidity
        dto.pressure = entity.pressure
        return dto

    @staticmethod
    def entityToExportDto(entity: BmeEntity):
        dto = ExportBMEDto()
        dto.temperature = entity.temperature
        dto.gas = entity.gas
        dto.humidity = entity.humidity
        dto.pressure = entity.pressure
        dto.time = entity.time
        return dto

    @staticmethod
    def save(model):
        try:
            db.session.add(model)
            db.session.commit()
            print("Data saved!")
            return True
        except:
            db.session.rollback()
            return False

    @staticmethod
    def getAll():
        measurements = BmeEntity.query.all()
        return measurements
