class MapQuality:

    @staticmethod
    def mapValue(value):
        if value > 425000:
            return "Good"
        elif 425000 >= value > 390000:
            return "Average"
        else:
            return "Bad"