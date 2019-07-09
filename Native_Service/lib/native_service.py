from django.conf import settings
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import datetime
from Native_Service.models import NativePost


class STAGES:
    IN_QUEUE = "W KOLEJCE"
    WAITING_FOR_ACCEPT = "OCZEKIWANIE NA AKCEPTACJĘ"
    ACCEPTED = "ZLECENIE ZAAKCEPTOWANE"
    PAYMENT_DONE = "ZLECENIE OPŁACONE"
    IN_PROGRESS = "W TRAKCIE REALIZACJI"
    DONE = "ZLECENIE ZAKOŃCZONE"


class ProgressStages:
    """ The basic logic of the email alert system and orders support. """

    @staticmethod
    def in_queue_stage(data=None, url=None):
        EmailGenerator().customer_queue_alert_html(data)
        EmailGenerator().performer_queue_alert_html(data, url)

    @staticmethod
    def waiting_for_accept(data=None, url=None, secret_key=None):
        post = NativePost.objects.get(secret_key=secret_key)
        post.stage = STAGES.WAITING_FOR_ACCEPT
        post.save()
        EmailGenerator().customer_price_to_accept_html(data, url)

    @staticmethod
    def accepted_stage(data=None, secret_key=None):
        post = NativePost.objects.get(secret_key=secret_key)
        post.stage = STAGES.ACCEPTED
        post.save()
        EmailGenerator().performer_order_accepted_html(data)

    @staticmethod
    def payment_done_stage(data=None, secret_key=None):
        post = NativePost.objects.get(secret_key=secret_key)
        post.stage = STAGES.PAYMENT_DONE
        post.save()
        EmailGenerator.customer_payment_done_html(data)

    @staticmethod
    def in_progress_stage(secret_key=None):
        post = NativePost.objects.get(secret_key=secret_key)
        post.stage = STAGES.IN_PROGRESS
        post.save()

    @staticmethod
    def done_stage(secret_key=None):
        post = NativePost.objects.get(secret_key=secret_key)
        post.stage = STAGES.DONE
        post.save()


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
    def performer_queue_alert_html(data=None, url=None):
        data["url"] = url
        subject, from_email = "Nowe zlecenie!", settings.SENDER
        text_message = f"Nowe zlecenie! {url}"

        msg_html = render_to_string("emails/performer_queue_alert.html", data)
        msg = EmailMultiAlternatives(
            subject, text_message, from_email, settings.PERFORMERS_LIST
        )
        msg.attach_alternative(msg_html, "text/html")
        msg.send()

    @staticmethod
    def customer_queue_alert_html(data=None):
        recipients_list = [data["email"]]
        subject, from_email = "Wycena zlecenia w NativeService!", settings.SENDER
        text_message = f"Wyceniamy Twoje zlecenie, czekaj na kontakt!"

        msg_html = render_to_string("emails/customer_queue_alert.html", data)
        msg = EmailMultiAlternatives(subject, text_message, from_email, recipients_list)
        msg.attach_alternative(msg_html, "text/html")
        msg.send()

    @staticmethod
    def customer_price_to_accept_html(data=None, url=None):
        data["url"] = url
        recipients_list = [data["email"]]
        subject, from_email = "Wycena zlecenia gotowa!", settings.SENDER
        text_message = f"Oto Twoja wycena, sprawdź link. {url}"

        msg_html = render_to_string("emails/customer_price_to_accept.html", data)
        msg = EmailMultiAlternatives(subject, text_message, from_email, recipients_list)
        msg.attach_alternative(msg_html, "text/html")
        msg.send()

    @staticmethod
    def performer_order_accepted_html(data=None):
        subject, from_email = "Warunki zaakceptowane!", settings.SENDER
        text_message = f"Użytkownik zaakceptował warunki! Oczekiwanie na płatność."

        msg_html = render_to_string(
            "emails/performer_price_accepted_waiting_for_payment.html", data
        )
        msg = EmailMultiAlternatives(
            subject, text_message, from_email, settings.PERFORMERS_LIST
        )
        msg.attach_alternative(msg_html, "text/html")
        msg.send()

    @staticmethod
    def customer_payment_done_html(data=None):
        recipients_list = [data["email"]]
        subject, from_email = "Płatność zrealizowana.", settings.SENDER
        text_message = f"Płatność zrealizowana, czekaj na kolejne wiadomości."

        msg_html = render_to_string("emails/customer_payment_done.html", data)
        msg = EmailMultiAlternatives(subject, text_message, from_email, recipients_list)
        msg.attach_alternative(msg_html, "text/html")
        msg.send()
