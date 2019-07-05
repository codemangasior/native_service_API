import os
from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
import datetime

os.environ["DJANGO_SETTINGS_MODULE"] = "Native_Service.settings_module"


class STAGES:
    IN_QUEUE = "in_queue"
    PRICING_IN_PROGRESS = "pricing_in_progress"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class ProgressStages:
    """ Basic logic of email alert system. """

    @staticmethod
    def in_queue_stage(data=None, files=None, url=None, secret_key=None):
        # todo emails needs new files urls
        EmailGenerator().performer_queue_alert_email(data, files, url, secret_key)
        EmailGenerator().customer_queue_alert_email(data, files)

    @staticmethod
    def pricing_in_progress_stage(data=None, url=None):
        EmailGenerator().customer_price_accept_email(data, url)

    @staticmethod
    def accepted_stage():
        pass

    @staticmethod
    def in_progress_stage():
        pass

    @staticmethod
    def done_stage():
        pass


class SecretKey:
    @staticmethod
    def create():
        """ Method generates secret keys. """
        return get_random_string(12)


class UrlsGenerator:
    """ The class contains all methods generating URL's"""

    @staticmethod
    def view_finalpricing_url(secret_key):
        """ Method generates url for performer to make some price. """
        return f"{settings.HOST_URL}/final_pricing/{secret_key}/"

    @staticmethod
    def view_priceforcustomer_url(secret_key):
        """ Method generates url for customer to see price. """
        return f"{settings.HOST_URL}/price_for_you/{secret_key}/"

    @staticmethod
    def view_priceaccepteddotpay_url(secret_key):
        """ Method generates url for customer for price accept. """
        return f"{settings.HOST_URL}/price_accepted/{secret_key}/"

    @staticmethod
    def view_filelistview_url(secret_key):
        """ Method generates url for performer to see list of files. """
        return f"{settings.HOST_URL}/file_list/{secret_key}/"

    @staticmethod
    def list_files_urls_create(file_data, secret_key):
        """ Method generates uploaded file list. """
        return [
            f"{settings.HOST_URL}{settings.MEDIA_URL}uploads/{datetime.date.today()}/{secret_key}/{f}\n".replace(
                " ", ""
            )
            for f in file_data
        ]

    @staticmethod
    def list_order_files_for_filelistview(secret_key, coded_files_list, url_date):
        """ Method generates url for performer to take look at file list. """
        return [
            f"{settings.HOST_URL}/media/uploads/{url_date}/{secret_key}/{f}"
            for f in coded_files_list
        ]


class EmailGenerator:
    """ The class contains all email sending methods. """

    @staticmethod
    def performer_queue_alert_email(
    data, files="No files.", url="No url.", secret_key=None
    ):
        recipients_list = settings.PERFORMERS_LIST

        send_mail(
            f"Nowe zlecenie!",
            f"Wejdź na https://nativeservice.pl/admin/ i sprawdź co na Ciebie czeka.\n"
            f"Imię: {data['name']}\n"
            f"Nazwisko: {data['last_name']}\n"
            f"Nazwa zlecenia: {data['title']}\n"
            f"Email: {data['email']}\n"
            f"Telefon: {data['phone']}\n"
            f"Data najpóźniejszej realizacji: {data['date_to_be_done']}\n"
            f"Opis: {data['description']}\n"
            f"{''.join(UrlsGenerator().list_files_urls_create(files, secret_key))}"
            f"\n\nTen email został'wygenerowany automatycznie. Prosimy o nie odpowiadanie na wiadomość.\n"
            f"Wejdź na {url} i dokonaj wyceny.",
            settings.SENDER,
            recipients_list,
            fail_silently=False,
        )

    @staticmethod
    def customer_queue_alert_email(data, files="No files."):
        recipients_list = [data["email"]]

        send_mail(
            f"Native Service - wycena zlecenia.",
            f"Witaj {data['name']}\n"
            f"Twój unikalny kod do dalszej realizacji zlecenia to: {data['secret_key']}.\n"
            f"Twoja wycena '{data['title']}' oczekuje w kolejce! \n"
            f"Wyceny zleceń wysłanych w godzinach od 8 rano do 20 realizujemy w ciągu 15 minut!\n"
            f"Oto Twoje dane: \n"
            f"Imię: {data['name']}\n"
            f"Nazwisko: {data['last_name']}\n"
            f"Nazwa zlecenia: {data['title']}\n"
            f"Email: {data['email']}\n"
            f"Telefon: {data['phone']}\n"
            f"Data najpóźniejszej realizacji {data['date_to_be_done']}\n"
            f"Opis: {data['description']}\n\n"
            f"\n\nTen email został'wygenerowany automatycznie. Prosimy o nie odpowiadanie na wiadomość.",
            settings.SENDER,
            recipients_list,
            fail_silently=False,
        )

    @staticmethod
    def customer_price_accept_email(data, url):
        recipients_list = [data["email"]]
        send_mail(
            f"Native Service - wycena zlecenia gotowa.",
            f"Witaj {data['name']}\n"
            f"Twoja wycena '{data['title']}' została zrealizowana! \n"
            f"Całkowity koszt usługi to {data['price']} zł\n"
            # todo |/ this time should be got by some 'time' method
            f"Czas realizacji to {data['time_to_get_ready']}.\n"
            f"Uwagi: {data['comments']}.\n"
            f"Aby zapoznać się ze szczegółami kliknij w link: {url}\n"
            f"\n\nTen email został'wygenerowany automatycznie. Prosimy o nie odpowiadanie na wiadomość.",
            settings.SENDER,
            recipients_list,
            fail_silently=False,
        )
