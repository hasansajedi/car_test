import calendar

from django.conf import settings
import datetime

from app.models import Wheel, Tire, Battery


class CarBuilder:
    __builder = None

    def setBuilder(self, builder):
        self.__builder = builder

    def getCar(self, battery_id, wheel_id, tire_id):
        car = Car()

        battery = self.__builder.getBattery(battery_id)
        car.setBattery(battery)

        wheel = self.__builder.getWheel(wheel_id)
        car.setWheel(wheel)

        tire = self.__builder.getTire(tire_id)
        car.setTire(tire)

        return car


# The whole product
class Car:
    def __init__(self):
        self.__battery = None
        self.__wheels = None
        self.__tire = None

    def setBattery(self, battery):
        self.__battery = battery

    def setWheel(self, wheel):
        self.__wheels = wheel

    def setTire(self, tire):
        self.__tire = tire

    def specification(self):
        return self.__battery.name, self.__wheels.name, self.__tire.name

    def calculate_price(self):
        percentage = lambda part, whole: float(whole) / 100 * float(part)
        car_base_price = settings.CAR_BASE_PRICE
        totalAmount = car_base_price + \
                      Battery.objects.get(id=self.__battery.id).amount + \
                      Wheel.objects.get(id=self.__wheels.id).amount + \
                      Tire.objects.get(id=self.__tire.id).amount
        today = datetime.date.today()
        last_date_of_month = self.last_friday_of_month(today.year, today.month)
        if last_date_of_month == today.day:
            return (percentage(int(settings.LAST_DAY_OF_MONTH_DISCOUNT), totalAmount),
                    float(settings.LAST_DAY_OF_MONTH_DISCOUNT))
        else:
            return totalAmount, 0.0

    def last_friday_of_month(self, year, month):
        return max(week[calendar.FRIDAY] for week in calendar.monthcalendar(year, month))


class Builder:
    def getBattery(self, battery_id):
        pass

    def getWheel(self, wheel_id):
        pass

    def getTire(self, tire_id):
        pass


class DataLabCarBuilder(Builder):
    def getBattery(self, battery_id):
        return Battery.objects.get(id=battery_id)

    def getWheel(self, wheel_id):
        return Wheel.objects.get(id=wheel_id)

    def getTire(self, tire_id):
        return Tire.objects.get(id=tire_id)


