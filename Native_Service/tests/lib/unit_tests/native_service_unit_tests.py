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

PRIORITY_CHOICE = [("WYSOKI", "WYSOKI"), ("STANDARD", "STANDARD"), ("NISKI", "NISKI")]

STAGE = [
    ("W KOLEJCE", "W KOLEJCE"),
    ("OCZEKIWANIE NA AKCEPTACJĘ", "OCZEKIWANIE NA AKCEPTACJĘ"),
    ("ZAAKCEPTOWANE", "ZAAKCEPTOWANE"),
    ("OPŁACONE", "OPŁACONE"),
    ("W TRAKCIE REALIZACJI", "W TRAKCIE REALIZACJI"),
    ("ZAKOŃCZONE", "ZAKOŃCZONE"),
    ("ODRZUCONE", "ODRZUCONE"),
]



@pytest.fixture
def test_native_service_url():
    return settings.HOST_URL


@pytest.fixture
def test_secret_key():
    return native_service.NSMethods.create_secret_key()


class FIXTURES:
    SECRET_KEY = test_secret_key
    DATETIME = datetime.datetime.now()
    DATE = datetime.date.today()

@pytest.mark.django_db
def nativepostmodel():
    order = NativePost.objects.create(
        category="Tłumaczenia",
        name="Łukasz",
        last_name="Gąsiorowski",
        title="Order title",
        priority="STANDARD",
        stage="W KOLEJCE",
        email="lukasz.gasiorowski92@gmail.com",
        phone="123456789",
        url_date=FIXTURES.DATETIME,
        create=FIXTURES.DATETIME,
        modified=FIXTURES.DATETIME,
        date_to_be_done=FIXTURES.DATE,
        description="description",
        secret_key=FIXTURES.SECRET_KEY,
        slug=FIXTURES.SECRET_KEY,
        time_to_get_ready=FIXTURES.DATE,
        price="1000",
        comments="Some comment to order",
    )
    order.save()
    return order


""" URL GENERATOR UNIT TEST """


def test_url_view_final_pricing():
    assert (
        native_service.UrlsGenerator.view_final_pricing(FIXTURES.SECRET_KEY)
        == f"{settings.HOST_URL}final_pricing/{FIXTURES.SECRET_KEY}/"
    )


def test_url_view_price_for_customer():
    assert (
        native_service.UrlsGenerator.view_price_for_customer(FIXTURES.SECRET_KEY)
        == f"{settings.HOST_URL}price_for_you/{FIXTURES.SECRET_KEY}/"
    )


def test_url_view_price_accepted_payu():
    assert (
        native_service.UrlsGenerator.view_price_accepted_dotpay(FIXTURES.SECRET_KEY)
        == f"{settings.HOST_URL}price_accepted/{FIXTURES.SECRET_KEY}/"
    )


def test_url_view_file_list():
    assert (
        native_service.UrlsGenerator.view_file_list_view(FIXTURES.SECRET_KEY)
        == f"{settings.HOST_URL}file_list/{FIXTURES.SECRET_KEY}/"
    )


def test_url_view_notify():
    assert (
        native_service.UrlsGenerator.view_notify(FIXTURES.SECRET_KEY)
        == f"{settings.HOST_URL}notify/"
    )


def test_url_view_successful_payment():
    assert (
        native_service.UrlsGenerator.view_successful_payment(FIXTURES.SECRET_KEY)
        == f"{settings.HOST_URL}successful_payment/{FIXTURES.SECRET_KEY}/"
    )


def test_url_view_order_in_progress():
    assert (
        native_service.UrlsGenerator.view_order_in_progress(FIXTURES.SECRET_KEY)
        == f"{settings.HOST_URL}in_progress/{FIXTURES.SECRET_KEY}/"
    )


def test_url_view_reject_order():
    assert (
        native_service.UrlsGenerator.view_reject_order(FIXTURES.SECRET_KEY)
        == f"{settings.HOST_URL}reject_order/{FIXTURES.SECRET_KEY}/"
    )


def test_url_view_done():
    assert (
        native_service.UrlsGenerator.view_done(FIXTURES.SECRET_KEY)
        == f"{settings.HOST_URL}order_done/{FIXTURES.SECRET_KEY}/"
    )


""" NSMethods UNIT TEST """


def test_create_secret_key():
    assert (native_service.NSMethods.create_secret_key().isprintable() == True)
    assert (native_service.NSMethods.create_secret_key().isalnum() == True)
    assert (native_service.NSMethods.create_secret_key().isascii() == True)
    for i in native_service.NSMethods.create_secret_key():
        assert i.isspace() == False


@pytest.mark.django_db
def test_get_nativepost_data():
    nativepostmodel()
    model = native_service.NSMethods.get_nativepost_data(FIXTURES.SECRET_KEY)
    assert model["title"] == "Order title"


def test_date_today():
    assert (native_service.NSMethods.date_today()[0] == str(FIXTURES.DATE.year))
    assert (native_service.NSMethods.date_today()[1] == str('{:02d}'.format(FIXTURES.DATE.month)))
    assert (native_service.NSMethods.date_today()[2] == str('{:02d}'.format(FIXTURES.DATE.day)))

