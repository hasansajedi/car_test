from app.models import Wheel, Tire, Battery


class CarBuilder:
    __builder = None

    def setBuilder(self, builder):
        self.__builder = builder

    def getCar(self):
        car = Car()

        # First goes the body
        battery = self.__builder.getBattery()
        car.setBattery(battery)

        # Then engine
        tire = self.__builder.getTire()
        car.setTire(tire)

        # And four wheels
        i = 0
        while i < 4:
            wheel = self.__builder.getWheel()
            car.attachWheel(wheel)
            i += 1

        return car


# The whole product
class Car:
    def __init__(self):
        self.__battery = None
        self.__wheels = list()
        self.__tire = None

    def setBattery(self, battery):
        self.__battery = battery

    def attachWheel(self, wheel):
        self.__wheels.append(wheel)

    def setTire(self, tire):
        self.__tire = tire

    def specification(self):
        print("battery: %s" % self.__battery.name)
        print("tire: %d" % self.__tire.name)
        print("wheel: %d\'" % self.__wheels[0].name)


class Builder:
    def getWheel(self): pass

    def getTire(self): pass

    def getBattery(self): pass


class JeepBuilder(Builder):
    def getBattery(self):
        battery = Battery()
        battery.id = 1
        return battery

    def getWheel(self):
        wheel = Wheel()
        wheel.id = 1
        return wheel

    def getTire(self):
        tire = Tire()
        tire.id = 400
        return tire



def main():
    jeepBuilder = JeepBuilder()  # initializing the class

    director = CarBuilder()

    # Build Jeep
    print("Jeep")
    director.setBuilder(jeepBuilder)
    jeep = director.getCar()
    jeep.specification()
    print("")


if __name__ == "__main__":
    main()
