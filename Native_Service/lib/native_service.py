import os
from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

os.environ["DJANGO_SETTINGS_MODULE"] = "Native_Service.settings_module"


class STAGES:
    IN_QUEUE = "in_queue"
    PRICING_IN_PROGRESS = "pricing_in_progress"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class ProgressStages:
    """ Basic logic of email alert system. """

    def __init__(self, data=None, files=None, url=None, url_accept_price=None):
        self.current_stage = None
        self.data = data
        self.files = files
        self.url = url
        self.url_accept_price = url_accept_price

    def in_queue_stage(self):
        self.current_stage = STAGES.IN_QUEUE
        # todo emails needs new files urls
        EmailGenerator().performer_queue_alert_email(self.data, self.files, self.url)
        EmailGenerator().customer_queue_alert_email(self.data, self.files)

    def pricing_in_progress_stage(self):
        self.current_stage = STAGES.PRICING_IN_PROGRESS
        EmailGenerator().customer_price_accept_email(self.data, self.url)

    def accepted_stage(self):
        self.current_stage = STAGES.ACCEPTED

        pass

    def in_progress_stage(self):
        self.current_stage = STAGES.IN_PROGRESS
        pass

    def done_stage(self):
        self.current_stage = STAGES.DONE
        pass


class SecretKey:
    @staticmethod
    def create():
        """ Method generates secret keys. """
        return get_random_string(12)


class UrlsGenerator:
    """ The class contains all methods generating URL's"""

    def files_urls_list_creating(self, file_data):
        """ Method generates uploaded file list. """
        return [
            f"{settings.HOST_URL}{settings.MEDIA_URL}{f}\n".replace(" ", "_")
            for f in file_data
        ]

    def final_pricing_url_genrator(self, secret_key):
        """ Method generates url for performer to make some price. """
        return f"{settings.LOCAL_HOST_URL}/final_pricing/{secret_key}/"

    def accept_view_url_generator(self, secret_key):
        """ Method generates url for customer to see price. """
        return f"{settings.LOCAL_HOST_URL}/price_for_you/{secret_key}/"

    def accept_price_url_generator(self, secret_key):
        """ Method generates url for customer for price accept. """
        return f"{settings.LOCAL_HOST_URL}/price_accepted/{secret_key}/"


class EmailGenerator:
    """ The class contains all email sending methods. """

    def performer_queue_alert_email(self, data, files="No files.", url="No url."):
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
            f"{''.join(UrlsGenerator().files_urls_list_creating(files))}"
            f"\n\nTen email został'wygenerowany automatycznie. Prosimy o nie odpowiadanie na wiadomość.\n"
            f"Wejdź na {url} i dokonaj wyceny.",
            settings.SENDER,
            recipients_list,
            fail_silently=False,
        )

    def customer_queue_alert_email(self, data, files="No files."):
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
            f"Opis: {data['description']}\n"
            f"{''.join(UrlsGenerator().files_urls_list_creating(files))}"
            f"\n\nTen email został'wygenerowany automatycznie. Prosimy o nie odpowiadanie na wiadomość.",
            settings.SENDER,
            recipients_list,
            fail_silently=False,
        )

    def customer_price_accept_email(self, data, url):
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
