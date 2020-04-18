from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from app.models import *
from .models import User


class BatteryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'amount']

    class Meta:
        model = Battery

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)


class WheelAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'amount']

    class Meta:
        model = Wheel

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)


class TireAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'amount']

    class Meta:
        model = Tire

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'mobile', 'email', 'created_on']

    class Meta:
        model = OrderModel

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Battery, BatteryAdmin)
admin.site.register(Wheel, WheelAdmin)
admin.site.register(Tire, TireAdmin)
admin.site.register(OrderModel, OrderAdmin)
admin.site.register(User, UserAdmin)

admin.site.register(Tier_condition)
admin.site.register(Wheel_condition)
