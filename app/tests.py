from django.test import TestCase

from app.builder import DataLabCarBuilder, CarBuilder
from app.models import Battery, Wheel, Tire, OrderModel


class BatteryTestCase(TestCase):
    def setUp(self):
        Battery.objects.create(name="battery_1", amount=10.0)
        Battery.objects.create(name="battery_2", amount=50.0)

    def test_batteries_amount(self):
        battery_1 = Battery.objects.get(name="battery_1")
        battery_2 = Battery.objects.get(name="battery_2")
        self.assertEqual(battery_1.amount, 10.0)
        self.assertEqual(battery_2.amount, 50.0)


class WheelTestCase(TestCase):
    def setUp(self):
        Wheel.objects.create(name="wheel_1", amount=10.0)
        Wheel.objects.create(name="wheel_2", amount=50.0)

    def test_wheel_amount(self):
        wheel_1 = Wheel.objects.get(name="wheel_1")
        wheel_2 = Wheel.objects.get(name="wheel_2")
        self.assertEqual(wheel_1.amount, 10.0)
        self.assertEqual(wheel_2.amount, 50.0)


class TireTestCase(TestCase):
    def setUp(self):
        Tire.objects.create(name="tire_1", amount=10.0)
        Tire.objects.create(name="tire_2", amount=50.0)

    def test_tire_amount(self):
        tire_1 = Tire.objects.get(name="tire_1")
        tire_2 = Tire.objects.get(name="tire_2")
        self.assertEqual(tire_1.amount, 10.0)
        self.assertEqual(tire_2.amount, 50.0)


class OrderModelTestCase(TestCase):
    def setUp(self):
        battery = Battery.objects.create(name="battery_1", amount=10.0)
        wheel = Wheel.objects.create(name="wheel_1", amount=10.0)
        tire = Tire.objects.create(name="tire_1", amount=10.0)

        OrderModel.objects.create(fullname='Hasan Sajedi', mobile='15237931461',
                                  email='hassansajedi@gmail.com',
                                  address='Antoninusstraße 54', city='Frankfurt am Main', state=5,
                                  zip='60439',
                                  battery=battery, wheel=wheel, tier=tire, discount=0.0, total_cost=1000)

    def test_order_can_submit(self):
        order_1 = OrderModel.objects.get(mobile="15237931461")
        self.assertEqual(order_1.fullname, "Hasan Sajedi")


class CarTestCase(TestCase):
    def setUp(self):
        self.battery = Battery.objects.create(name="battery_1", amount=10.0)
        self.wheel = Wheel.objects.create(name="wheel_1", amount=10.0)
        self.tire = Tire.objects.create(name="tire_1", amount=10.0)

    def test_car_has_configured(self):
        dataLabBuilder = DataLabCarBuilder()  # initializing the class
        car = CarBuilder()

        car.setBuilder(dataLabBuilder)
        x = car.getCar(self.battery.id, self.wheel.id, self.tire.id)
        x.setBattery(self.battery)
        x.setWheel(self.wheel)
        x.setTire(self.tire)

        self.assertIsNotNone(x.calculate_price())
