import datetime

from django.conf import settings

from Native_Service.lib import native_service
from Native_Service.models import NativePost
import pytest


""" Unit tests """

CATEGORY_CHOICE = [
    ("REPREZENTOWANIE FIRM", "REPREZENTOWANIE FIRM"),
    ("SPRAWY URZĘDOWE", "SPRAWY URZĘDOWE"),
    ("PRACA MIESZKANIE AUTO", "PRACA MIESZKANIE AUTO"),
    ("TŁUMACZENIA", "TŁUMACZENIA"),
]

PRIORITY_CHOICE = [
    ("WYSOKI", "WYSOKI"),
    ("STANDARD", "STANDARD"),
    ("NISKI", "NISKI"),
]

STAGE = [
    ("W KOLEJCE", "W KOLEJCE"),
    ("OCZEKIWANIE NA AKCEPTACJĘ", "OCZEKIWANIE NA AKCEPTACJĘ"),
    ("ZAAKCEPTOWANE", "ZAAKCEPTOWANE"),
    ("OPŁACONE", "OPŁACONE"),
    ("W TRAKCIE REALIZACJI", "W TRAKCIE REALIZACJI"),
    ("ZAKOŃCZONE", "ZAKOŃCZONE"),
    ("ODRZUCONE", "ODRZUCONE"),
]

DATETIME = datetime.datetime.now()

DATE = datetime.date.today()


@pytest.fixture
def test_native_service_url():
    return settings.HOST_URL


@pytest.fixture
def test_secret_key():
    return native_service.NSMethods.create_secret_key()


SECRET_KEY = test_secret_key


@pytest.fixture
def nativepost_model_object():

    order = NativePost
    order.category = "TŁUMACZENIA"
    order.name = "Łukasz"
    order.last_name = "Gąsiorowski"
    order.title = "Order title"
    order.priority = "STANDARD"
    order.stage = "W KOLEJCE"
    order.email = "lukasz.gasiorowski92@gmail.com"
    order.phone = "123456789"
    order.url_date = DATETIME
    order.create = DATETIME
    order.modified = DATETIME
    order.date_to_be_done = DATE
    order.description = "description"
    order.secret_key = SECRET_KEY
    order.slug = SECRET_KEY
    order.time_to_get_ready = DATE
    order.price = "1000"
    order.comments = "Some comment to order"


# at the end of every nativemodel test
def nativepost_model_object_delete():
    NativePost.objects.filter(secret_key=SECRET_KEY).delete()


""" URL GENERATOR UNIT TEST """


def test_url_view_final_pricing():
    assert (native_service.UrlsGenerator.view_final_pricing(SECRET_KEY) == f"{settings.HOST_URL}final_pricing/{SECRET_KEY}/")


def test_url_view_price_for_customer():
    assert (native_service.UrlsGenerator.view_price_for_customer(SECRET_KEY) == f"{settings.HOST_URL}price_for_you/{SECRET_KEY}/")


def test_url_view_price_accepted_payu():
    assert (native_service.UrlsGenerator.view_price_accepted_dotpay(SECRET_KEY) == f"{settings.HOST_URL}price_accepted/{SECRET_KEY}/")


def test_url_view_file_list():
    assert (native_service.UrlsGenerator.view_file_list_view(SECRET_KEY) == f"{settings.HOST_URL}file_list/{SECRET_KEY}/")


def test_url_view_notify():
    assert (native_service.UrlsGenerator.view_notify(SECRET_KEY) == f"{settings.HOST_URL}notify/")


def test_url_view_successful_payment():
    assert (native_service.UrlsGenerator.view_successful_payment(SECRET_KEY) == f"{settings.HOST_URL}successful_payment/{SECRET_KEY}/")


def test_url_view_order_in_progress():
    assert (native_service.UrlsGenerator.view_order_in_progress(SECRET_KEY) == f"{settings.HOST_URL}in_progress/{SECRET_KEY}/")


def test_url_view_reject_order():
    assert (native_service.UrlsGenerator.view_reject_order(SECRET_KEY) == f"{settings.HOST_URL}reject_order/{SECRET_KEY}/")


def test_url_view_done():
    assert (native_service.UrlsGenerator.view_done(SECRET_KEY) == f"{settings.HOST_URL}order_done/{SECRET_KEY}/")
