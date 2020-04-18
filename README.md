# DATA:LAB - Tech Check

This application uploaded on [Github](https://github.com/hasansajedi/car_test) and test automated with CircleCI.

## Installation
To build, test and deploy application please, run bash.sh file in root direcory:

```bash
> ./bash.sh
```
or
```bash
> python3.8 -m venv venv
> source venv/bin/activate
> pip install --upgrade pip
> pip install -r requirements.txt
> source .envrc
> python ./manage.py migrate
> python ./manage.py test
> pipenv run python manage.py runserver

```

## Usage

Before use this application you should be login as a 'admin' or 'guest' user. The password of users is 'qazWSX@123'.

Urls list:
> Login= 127.0.0.1:8000/login
>
> Logout= 127.0.0.1:8000/logout
>
> Login= 127.0.0.1:8000/login
>
> Configure= 127.0.0.1:8000/configure
>
> report= 127.0.0.1:8000/report

## Features

1. Authentication users.
2. Authorization services.
3. Calculate last friday of month and make discount per each order.
4. Select wheels and tires according to conditions.
5. Get some information of users before submit order.
6. Show all information about user order configuration before submit order. 
7. Show an UI to user after submit order.
8. The average price of all submitted car configurations.
9. The percentage distribution of each of the options that have been configured.
10. The 95 percentile for the price of the already configured cars.
11. The number of cars and the average price sold with the Friday discount
12. The number of cars and the average price sold without the Friday discount

## Settings

```python
CAR_BASE_PRICE = 12000 # The base price for the car is 12.000 euros
REPORT_PAGINATION_NUMBER = 10 # The number of pagination in report page
LAST_DAY_OF_MONTH_DISCOUNT = 20 # special discount of 2.000 euros every last Friday of the month.

LOGIN_REDIRECT_URL = '/configure' # Redirect url after user logged in.
LOGOUT_REDIRECT_URL = '/login/' # Url after user logged out. 

LOGIN_URL = '/login/' # Login URL
AUTH_USER_MODEL = 'app.User' # Customized user model.
```