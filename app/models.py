from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser

import arrow

from phonenumber_field.modelfields import PhoneNumberField
from shortuuidfield import ShortUUIDField


# Create your models here.
class Battery(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, null=False)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.0, null=False)

    def __str__(self):
        return self.name + ": " + (str(self.amount) + " €" if self.amount > 0 else "included in the base price")


class Wheel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, null=False)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.0, null=False)

    def __str__(self):
        return self.name + ": " + (str(self.amount) + " €" if self.amount > 0 else "included in base price")


class Tire(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, null=False)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.0, null=False)

    def __str__(self):
        return self.name + ": " + (str(self.amount) + " €" if self.amount > 0 else "included in base price")


class Tier_condition(models.Model):
    wheel_id = models.ForeignKey(Wheel, on_delete=models.CASCADE)
    tier_id = models.ForeignKey(Tire, on_delete=models.CASCADE)

    def __str__(self):
        return self.tier_id.name + " available on model of " + self.wheel_id.name + " wheel"


class Wheel_condition(models.Model):
    battery_id = models.ForeignKey(Battery, on_delete=models.CASCADE)
    wheel_id = models.ForeignKey(Wheel, on_delete=models.CASCADE)

    def __str__(self):
        return self.wheel_id.name + " available on model of " + self.battery_id.name + " battery"


class OrderModel(models.Model):
    STATES = (
        (1, 'Baden-Württemberg'),
        (2, 'Bavaria (Bayern)'),
        (3, 'Berlin'),
        (4, 'Brandenburg'),
        (5, 'Bremen'),
        (6, 'Hamburg'),
        (7, 'Hesse (Hessen)'),
        (8, 'Lower Saxony (Niedersachsen)'),
        (9, 'Mecklenburg-Vorpommern'),
        (10, 'North Rhine-Westphalia (Nordrhein-Westfalen)'),
        (11, 'Rhineland-Palatinate (Rheinland-Pfalz)'),
        (12, 'Saarland'),
        (13, 'Saxony (Sachsen)'),
        (14, 'Saxony-Anhalt (Sachsen-Anhalt)'),
        (15, 'Schleswig-Holstein'),
        (16, 'Thuringia (Thüringen)'),
    )

    id = models.AutoField(primary_key=True)
    fullname = models.CharField(null=False, blank=False, max_length=250)
    mobile = PhoneNumberField(blank=False)
    email = models.EmailField(max_length=70, null=False, blank=False)
    address = models.CharField(null=False, blank=False, max_length=250)
    city = models.CharField(null=False, blank=False, max_length=70)
    state = models.IntegerField(null=False, choices=STATES)
    zip = models.CharField(null=False, max_length=20)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    uuid = ShortUUIDField(null=True, unique=True)
    battery = models.ForeignKey(Battery, on_delete=models.CASCADE)
    wheel = models.ForeignKey(Wheel, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tire, on_delete=models.CASCADE)
    discount = models.DecimalField(null=False, default=0, max_digits=3, decimal_places=2)
    total_cost = models.DecimalField(null=False, default=0, max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return u'%s' % self.fullname

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()


class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'

    '''
    (<django.db.models.fields.AutoField: id>, 
    <django.db.models.fields.CharField: password>, 
    <django.db.models.fields.DateTimeField: last_login>, 
    <django.db.models.fields.BooleanField: is_superuser>, 
    <django.db.models.fields.CharField: username>, 
    <django.db.models.fields.CharField: first_name>, 
    <django.db.models.fields.CharField: last_name>, 
    <django.db.models.fields.EmailField: email>, 
    <django.db.models.fields.BooleanField: is_staff>, 
    <django.db.models.fields.BooleanField: is_active>, 
    <django.db.models.fields.DateTimeField: date_joined>)
    '''
