import calendar
import json
import datetime
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from app.builder import DataLabCarBuilder, CarBuilder
from app.forms import OrderForm
from app.models import *


@login_required
def configure(request):
    """
    Load items in /configure.
    :return: context.
    """
    if request.method == "POST":  # If checkout form submitted, parse all fields posted from form here to save order.
        form = OrderForm(request.POST)  # Cast form posted by request to OrderForm.
        if form.is_valid():  # Check form must be valid.
            # try:
            data = request.POST.dict()  # Get all data filled in our form.
            fullname = data.get('fullname', None)  # Get fullname field value.
            battery_id = data.get('battery_id', None)  # Get battery_id field value.
            wheel_id = data.get('wheel_id', None)  # Get wheel_id field value.
            tire_id = data.get('tire_id', None)  # Get tire_id field value.

            battery = Battery.objects.get(id=battery_id)  # Check Battery is exist.
            wheel = Wheel.objects.get(id=wheel_id)  # Check Wheel is exist.
            tire = Tire.objects.get(id=tire_id)  # Check Tire is exist.

            totalAmount, discount = get_car(battery, wheel, tire)  # Calculate all cost of order configuration.

            form = form.save(commit=False)  # Disable commit in our form and then pass data manually.
            form.battery_id = battery.id
            form.wheel_id = wheel.id
            form.tier_id = tire.id
            form.discount = discount
            form.total_cost = totalAmount

            form.save()  # Submit form and save order.

            # Sent data to show in receipt of order.
            return render(request, "app/order.html", {'fullname': fullname,
                                                      'battery': battery.amount,
                                                      'wheel': wheel.amount,
                                                      'tire': tire.amount,
                                                      'baseAmount': settings.CAR_BASE_PRICE,
                                                      'totalAmount': totalAmount,
                                                      'discount': discount,
                                                      })
        # except Exception as e:
        #     print(e)
        else:
            err = form.errors
            return render(request, 'app/order.html', {'form': form, 'error': err})
    else:
        form = OrderForm()
        battery = Battery.objects.all()
        return render(request, "app/order.html", {'battery': battery,
                                                  'form': form})


@login_required
def checkout(request, battery_id, wheel_id, tire_id):
    """
    :param battery_id: Id od battery instance.
    :param wheel_id: Id od wheel instance.
    :param tire_id: Id od tire instance.
    :return: List of JSON.
    """
    if request.is_ajax():
        car_base_price = settings.CAR_BASE_PRICE  # Get value of base car price.
        battery = Battery.objects.get(id=battery_id)  # Check Battery is exist.
        wheel = Wheel.objects.get(id=wheel_id)  # Check wheel is exist.
        tire = Tire.objects.get(id=tire_id)  # Check tire is exist.

        totalAmount, discount = get_car(battery, wheel, tire)  # Calculate all cost of order configuration.

        # Sent data to show in last step of order in checkout.
        json_res = [dict(base_amount=str(car_base_price),
                         battery_amount=str(battery.amount),
                         wheel_amount=str(wheel.amount),
                         tire_amount=str(tire.amount),
                         discount=str(discount),
                         total_amount=str(totalAmount))]
        # Return the results
        return HttpResponse(json.dumps(json_res), content_type='application/json')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def report(request):
    """
    :return: List of orders submitted and some of statistics information.
    """
    if request.user.is_superuser:  # check user is admin to access this page.
        report_orders = OrderModel.objects.all().order_by('-id')  # Load all data in orders submitted.

        report_orders_count = report_orders.count()  # Get count of orders.
        # calculate average price for all orders.
        average_price = sum([item.total_cost for item in report_orders]) / report_orders_count

        # calculate all orders submitted out of friday discount (count and average).
        without_firday_discount = OrderModel.objects.filter(discount=Decimal('0.0'))
        without_firday_discount_average_price = (sum([item.total_cost for item in
                                                      without_firday_discount]) / without_firday_discount.count()) if without_firday_discount.count() > 0 else 0

        # calculate all orders submitted in friday discount (count and average).
        firday_discount = OrderModel.objects.filter(discount__gt=Decimal('0.01'))
        firday_discount_average_price = (sum([item.total_cost for item in
                                              firday_discount]) / firday_discount.count()) if firday_discount.count() > 0 else 0

        # calculate percentage distribution of all options that configured in orders submitted (percentage and list
        # of options).
        percentage_distribution = []
        x = OrderModel.objects.raw(
            'SELECT id, count(*) as cnt, battery_id,wheel_id, tier_id from app_ordermodel GROUP BY battery_id, wheel_id,tier_id;')
        for item in x:
            percentage_distribution.append(
                [float("{:.1f}".format(((item.cnt / report_orders_count) * 100))),
                 Battery.objects.get(id=item.battery_id).name,
                 Wheel.objects.get(id=item.wheel_id).name,
                 Tire.objects.get(id=item.tier_id).name])

        # connect our queryset to paginator
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

        # Sent data to show in report page.
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
        return HttpResponse('Unauthorized', status=401)  # if user is not authorized return error.


@login_required
def check_available_wheel_for_battery(request, battery_id):
    """
    :param battery_id: Id od battery instance
    :return: List of JSON
    """
    if request.is_ajax():  # Check our request is ajax.
        battery = Battery.objects.get(id=battery_id)  # Get battery instance is exist.
        lst = []
        wheel = Wheel.objects.all()
        for item in wheel:  # for each record in wheel check in wheel_condition table
            qs = Wheel_condition.objects.filter(wheel_id=item.id)
            if qs.count() == 0:  # if record in wheel_condition table is not exist add to available items
                lst.append(item.id)
            else:  # Item has condition(s)
                for x in qs:
                    # if battery_id.id in wheel_condition is equal with battery.id then add to available items
                    if x.battery_id.id == battery.id:
                        lst.append(item.id)

        wheels = Wheel.objects.filter(id__in=lst)  # Get list of wheel taht available to show.

        json_res = []
        # Iterate over wheels and add to array
        for item in wheels:
            json_obj = dict(id=item.id, name=item.name, amount=str(item.amount), title=str(item))
            json_res.append(json_obj)

        # Return the results
        return HttpResponse(json.dumps(json_res), content_type='application/json')


@login_required
def check_available_tire_for_wheel(request, wheel_id):
    """
    :param wheel_id: Id od wheel instance
    :return: List of JSON
    """
    if request.is_ajax():  # Check our request is ajax.
        wheel = Wheel.objects.get(id=wheel_id)  # Get wheel instance is exist.
        lst = []
        tires = Tire.objects.all()
        for item in tires:  # for each record in tires check in tier_condition table
            qs = Tier_condition.objects.filter(tier_id=item.id)
            if qs.count() == 0:  # if record in tier_condition table is not exist add to available items
                lst.append(item.id)
            else:  # Item has condition(s)
                for x in qs:
                    # if wheel_id.id in wheel_condition is equal with wheel.id then add to available items
                    if x.wheel_id.id == wheel.id:
                        lst.append(item.id)

        tires = Tire.objects.filter(id__in=lst)  # Get list of wheel taht available to show.

        json_res = []
        # Iterate over tires and add to array
        for item in tires:
            json_obj = dict(id=item.id, name=item.name, amount=str(item.amount), title=str(item))
            json_res.append(json_obj)

        # Return the results
        return HttpResponse(json.dumps(json_res), content_type='application/json')


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


def get_car(battery, wheel, tire):
    dataLabBuilder = DataLabCarBuilder()  # initializing the class
    car = CarBuilder()

    car.setBuilder(dataLabBuilder)
    x = car.getCar(battery.id, wheel.id, tire.id)
    x.setBattery(battery)
    x.setWheel(wheel)
    x.setTire(tire)
    return x.calculate_price()
