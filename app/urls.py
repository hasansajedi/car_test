from django.urls import path

from .views import (
    configure,
    check_available_wheel_for_battery,
    check_available_tire_for_wheel,
    checkout,
    report,
    login_user,
    logout_user)

urlpatterns = [
    path(r'', configure, name='configure'),
    path(r'report/', report, name='report'),
    path(r'configure/', configure, name='configure'),
    path(r'check_available_wheel_for_battery/<int:battery_id>', check_available_wheel_for_battery,
         name='check_available_wheel_for_battery'),
    path(r'check_available_tire_for_wheel/<int:wheel_id>', check_available_tire_for_wheel,
         name='check_available_tire_for_wheel'),
    path(r'checkout/<int:battery_id>/<int:wheel_id>/<int:tire_id>', checkout,
         name='checkout'),
    path(r'login/', login_user, name='login'),
    path(r'logout/', logout_user, name='logout'),
]
