import calendar
import json
import datetime
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, QuerySet, Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from app.forms import OrderForm
from app.models import *


@login_required
def configure(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                data = request.POST.dict()
                fullname = data.get('fullname', None)
                battery_id = data.get('battery_id', None)
                wheel_id = data.get('wheel_id', None)
                tire_id = data.get('tire_id', None)

                battery = Battery.objects.get(id=battery_id)
                wheel = Wheel.objects.get(id=wheel_id)
                tire = Tire.objects.get(id=tire_id)

                totalAmount, discount = calculate_cost(battery.amount, wheel.amount, tire.amount)

                form = form.save(commit=False)
                form.battery_id = battery.id
                form.wheel_id = wheel.id
                form.tier_id = tire.id
                form.discount = discount
                form.total_cost = totalAmount

                form.save()
                return render(request, "app/order.html", {'fullname': fullname,
                                                          'battery': battery.amount,
                                                          'wheel': wheel.amount,
                                                          'tire': tire.amount,
                                                          'baseAmount': settings.CAR_BASE_PRICE,
                                                          'totalAmount': totalAmount,
                                                          'discount': discount,
                                                          })
            except Exception as e:
                print(e)
        else:
            err = form.errors
            return render(request, 'app/order.html', {'form': form, 'error': err})
    else:
        form = OrderForm()
        battery = Battery.objects.all()
        return render(request, "app/order.html", {'battery': battery,
                                                  'form': form})


@login_required
def check_available_wheel_for_battery(request, battery_id):
    if request.is_ajax():
        battery = Battery.objects.get(id=battery_id)
        lst = []
        wheel = Wheel.objects.all()
        for item in wheel:
            qs = Wheel_condition.objects.filter(wheel_id=item.id)
            if qs.count() == 0:
                lst.append(item.id)
            else:
                for x in qs:
                    if x.battery_id.id == battery.id:
                        lst.append(item.id)

        wheels = Wheel.objects.filter(id__in=lst)
        # Create array
        json_res = []

        # Iterate over results and add to array
        for item in wheels:
            json_obj = dict(id=item.id, name=item.name, amount=str(item.amount), title=str(item))
            json_res.append(json_obj)

        # Return the results
        return HttpResponse(json.dumps(json_res), content_type='application/json')


@login_required
def check_available_tire_for_wheel(request, wheel_id):
    if request.is_ajax():
        wheel = Wheel.objects.get(id=wheel_id)
        lst = []
        tires = Tire.objects.all()
        for item in tires:
            qs = Tier_condition.objects.filter(tier_id=item.id)
            if qs.count() == 0:
                lst.append(item.id)
            else:
                for x in qs:
                    if x.wheel_id.id == wheel.id:
                        lst.append(item.id)

        tires = Tire.objects.filter(id__in=lst)
        # Create array
        json_res = []

        # Iterate over results and add to array
        for item in tires:
            json_obj = dict(id=item.id, name=item.name, amount=str(item.amount), title=str(item))
            json_res.append(json_obj)

        # Return the results
        return HttpResponse(json.dumps(json_res), content_type='application/json')


@login_required
def checkout(request, battery_id, wheel_id, tire_id):
    if request.is_ajax():
        car_base_price = settings.CAR_BASE_PRICE
        battery = Battery.objects.get(id=battery_id)
        wheel = Wheel.objects.get(id=wheel_id)
        tire = Tire.objects.get(id=tire_id)

        totalAmount, discount = calculate_cost(battery.amount, wheel.amount, tire.amount)

        # Create array
        json_res = []
        json_res.append(dict(base_amount=str(car_base_price),
                             battery_amount=str(battery.amount),
                             wheel_amount=str(wheel.amount),
                             tire_amount=str(tire.amount),
                             discount=str(discount),
                             total_amount=str(totalAmount)))
        # Return the results
        return HttpResponse(json.dumps(json_res), content_type='application/json')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def report(request):
    if request.user.is_superuser:
        report_orders = OrderModel.objects.all().order_by('-id')

        report_orders_count = report_orders.count()
        average_price = sum([item.total_cost for item in report_orders]) / report_orders_count
        without_firday_discount = OrderModel.objects.filter(discount=Decimal('0.0'))
        without_firday_discount_average_price = (sum([item.total_cost for item in
                                                      without_firday_discount]) / without_firday_discount.count()) if without_firday_discount.count() > 0 else 0

        firday_discount = OrderModel.objects.filter(discount__gt=Decimal('0.01'))
        firday_discount_average_price = (sum([item.total_cost for item in
                                              firday_discount]) / firday_discount.count()) if firday_discount.count() > 0 else 0

        percentage_distribution = []
        x = OrderModel.objects.raw(
            'SELECT id, count(*) as cnt, battery_id,wheel_id, tier_id from app_ordermodel GROUP BY battery_id, wheel_id,tier_id;')
        for item in x:
            percentage_distribution.append(
                [float("{:.1f}".format(((item.cnt / report_orders_count) * 100))),
                 Battery.objects.get(id=item.battery_id).name,
                 Wheel.objects.get(id=item.wheel_id).name,
                 Tire.objects.get(id=item.tier_id).name])
        # print([sum(row[0] for row in percentage_distribution)])

        paginator = Paginator(report_orders, int(settings.REPORT_PAGINATION_NUMBER))
        page = request.GET.get('page')
        try:
            report_orders = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            report_orders = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            report_orders = paginator.page(paginator.num_pages)

        return render(request, "app/report.html", {'data': report_orders,
                                                   'report_orders_count': report_orders_count,
                                                   'average_price': float("{:.2f}".format(average_price)),
                                                   'firday_discount_count': firday_discount.count(),
                                                   'firday_discount_average_price': float(
                                                       "{:.2f}".format(firday_discount_average_price)),
                                                   'without_firday_discount': without_firday_discount.count(),
                                                   'without_firday_discount_average_price': float(
                                                       "{:.2f}".format(without_firday_discount_average_price)),
                                                   'percentage_distribution': percentage_distribution
                                                   })
    else:
        return HttpResponse('Unauthorized', status=401)


def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['user_name']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print('ssssss')
                return HttpResponseRedirect('/configure')
    context = {'foo': 'bar'}
    return render(request, 'registration/login.html', context)


def logout_user(request):
    logout(request)
    # messages.info(request, "Logged out successfully!")
    return HttpResponseRedirect('/login')


def calculate_cost(battery_amount, wheel_amount, tire_amount):
    percentage = lambda part, whole: float(whole) / 100 * float(part)
    car_base_price = settings.CAR_BASE_PRICE
    totalAmount = car_base_price + battery_amount + wheel_amount + tire_amount
    today = datetime.date.today()
    last_date_of_month = last_friday_of_month(today.year, today.month)
    if last_date_of_month == today.day:
        return (percentage(int(settings.LAST_DAY_OF_MONTH_DISCOUNT), totalAmount),
                float(settings.LAST_DAY_OF_MONTH_DISCOUNT))
    else:
        return totalAmount, 0.0


def last_friday_of_month(year, month):
    return max(week[calendar.FRIDAY] for week in calendar.monthcalendar(year, month))
