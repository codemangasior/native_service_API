import datetime
import time

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

from Native_Service.models import NativePost


class STAGES:
    IN_QUEUE = "W KOLEJCE"
    WAITING_FOR_ACCEPT = "OCZEKIWANIE NA AKCEPTACJĘ"
    ACCEPTED = "ZAAKCEPTOWANE"
    PAYMENT_DONE = "OPŁACONE"
    IN_PROGRESS = "W TRAKCIE REALIZACJI"
    DONE = "ZAKOŃCZONE"
    REJECTED = "ODRZUCONE"


class NSMethods:
    """ NativeService necessary methods. """

    @staticmethod
    def create_secret_key():
        """ Method generates secret keys. """
        return get_random_string(12)

    @staticmethod
    def get_nativepost_data(secret_key):
        """ Function returns all data from native post filtered with secret_key."""
        data = NativePost.objects.filter(secret_key=secret_key)

        data_dict = {}
        for i in data.values():
            data_dict.update(i)
        return data_dict

    @staticmethod
    def date_today():
        """ Returns tuple with actual values: YEAR, MONTH, DAY"""
        time = datetime.datetime.now()
        return time.strftime("%Y"), time.strftime("%m"), time.strftime("%d")


class ProgressStages:
    """ The basic logic of the email alert system and orders support. """

    @staticmethod
    def in_queue(data=None, url=None):
        EmailGenerator().customer_queue_alert_html(data)
        EmailGenerator().performer_queue_alert_html(data, url)

    @staticmethod
    def waiting_for_accept(data=None, url=None, secret_key=None):
        post = NativePost.objects.get(secret_key=secret_key)
        if data["stage"] == STAGES.IN_QUEUE:
            post.stage = STAGES.WAITING_FOR_ACCEPT
            post.save()
            EmailGenerator().customer_price_to_accept_html(data, url)
        else:
            raise PermissionError("The valuation is not in queue.")

    @staticmethod
    def accepted(data=None, secret_key=None):
        post = NativePost.objects.get(secret_key=secret_key)
        if data["stage"] == STAGES.WAITING_FOR_ACCEPT:
            post.stage = STAGES.ACCEPTED
            post.save()
            EmailGenerator().performer_order_accepted_html(data)
        else:
            raise PermissionError("The valuation is not waiting for accept.")

    @staticmethod
    def payment_done(data=None, secret_key=None, url=None):
        ALLOWED_STAGES = [STAGES.ACCEPTED, STAGES.REJECTED]
        post = NativePost.objects.get(secret_key=secret_key)
        if data["stage"] in ALLOWED_STAGES:
            post.stage = STAGES.PAYMENT_DONE
            post.save()
            EmailGenerator.customer_payment_done_html(data)
            EmailGenerator.performer_payment_done_html(data, url)

        else:
            raise PermissionError("The order stage is not 'ACCEPTED' at the moment.")

    @staticmethod
    def in_progress(data=None, secret_key=None, url=None):
        post = NativePost.objects.get(secret_key=secret_key)
        if data["stage"] == STAGES.PAYMENT_DONE:
            post.stage = STAGES.IN_PROGRESS
            post.save()
            EmailGenerator.customer_order_in_progress_html(data)
            EmailGenerator.performer_order_in_progress_html(data, url)
        else:
            raise PermissionError(
                "The order stage is not 'PAYMENT_DONE' at the moment."
            )

    @staticmethod
    def done(data=None, secret_key=None, attachment=None):
        # todo new field with end datetime
        post = NativePost.objects.get(secret_key=secret_key)
        if data["stage"] != STAGES.DONE:
            post.stage = STAGES.DONE
            post.save()
            EmailGenerator().customer_order_done_with_files(data, attachment)
        else:
            raise PermissionError("The order stage is already 'DONE' at the moment.")

    @staticmethod
    def order_rejected(data=None, secret_key=None):
        post = NativePost.objects.get(secret_key=secret_key)
        if data["stage"] != STAGES.REJECTED:
            post.stage = STAGES.REJECTED
            post.save()
            EmailGenerator.customer_order_rejected(data)
        else:
            raise PermissionError(
                "The order stage is already 'REJECTED' at the moment."
            )

    @staticmethod
    def correct_payment(secret_key=None):
        payment_done = False
        while payment_done != True:
            stage = NSMethods.get_nativepost_data(secret_key)["stage"]
            if stage == STAGES.PAYMENT_DONE:
                payment_done = True
            else:
                time.sleep(2)
            if stage == STAGES.REJECTED:
                break
        return payment_done

    @staticmethod
    def payment_rejected(data=None, secret_key=None):
        # todo email for rejected payment
        ALLOWED_STAGES = [STAGES.REJECTED, STAGES.ACCEPTED]
        post = NativePost.objects.get(secret_key=secret_key)
        if data["stage"] in ALLOWED_STAGES:
            post.stage = STAGES.REJECTED
            post.save()
        else:
            # todo when PayU returns previous operation 'canceled' after successful current transfer, system raise error
            PermissionError(
                "The order stage is not 'ACCEPTED' or 'REJECTED' at the moment."
            )


class UrlsGenerator:
    """ The class contains all methods generating URL's"""

    @staticmethod
    def view_final_pricing(secret_key):
        """ Method generates url for performer to make some price. """
        return f"{settings.HOST_URL}final_pricing/{secret_key}/"

    @staticmethod
    def view_price_for_customer(secret_key):
        """ Method generates url for customer to see price. """
        return f"{settings.HOST_URL}price_for_you/{secret_key}/"

    @staticmethod
    def view_price_accepted_payu(secret_key):
        """ Method generates url for customer for price accept. """
        return f"{settings.HOST_URL}price_accepted/{secret_key}/"

    @staticmethod
    def view_file_list_view(secret_key):
        """ Method generates url for performer to see list of files. """
        return f"{settings.HOST_URL}file_list/{secret_key}/"

    @staticmethod
    def view_notify(secret_key):
        """ Method generates url for PayU to sent request. """
        return f"{settings.HOST_URL}notify/"

    @staticmethod
    def view_successful_payment(secret_key):
        """ Method generates url for performer to see successful_payment view. """
        return f"{settings.HOST_URL}successful_payment/{secret_key}/"

    @staticmethod
    def view_order_in_progress(secret_key):
        """ Method generates url for performer to set stage on 'in_progress'. """
        return f"{settings.HOST_URL}in_progress/{secret_key}/"

    @staticmethod
    def view_reject_order(secret_key):
        """ Method generates url for performer to reject the order. """
        return f"{settings.HOST_URL}reject_order/{secret_key}/"

    @staticmethod
    def view_done(secret_key):
        """ Method generates url for performer to set stage on 'done'. """
        return f"{settings.HOST_URL}order_done/{secret_key}/"

    @staticmethod
    def list_order_files_for_file_list_view(secret_key, coded_files_list, url_date):
        """ Method generates url for performer to take look at file list. """
        return [
            f"{settings.HOST_URL}media/uploads/{url_date}/{secret_key}/{f}"
            for f in coded_files_list
        ]


class EmailGenerator:
    """ The class contains all email sending methods. """

    @staticmethod
    def performer_queue_alert_html(data=None, url=None):
        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        data.update({"url": url, "now": now})
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

    @staticmethod
    def performer_payment_done_html(data=None, url=None):
        data["url"] = url
        subject, from_email = "Zlecenie opłacone!", settings.SENDER
        text_message = f"Użytkownik opłacił zlecenie! Zmień status na 'in_progress'."

        msg_html = render_to_string("emails/performer_payment_done.html", data)
        msg = EmailMultiAlternatives(
            subject, text_message, from_email, settings.PERFORMERS_LIST
        )
        msg.attach_alternative(msg_html, "text/html")
        msg.send()

    @staticmethod
    def customer_order_in_progress_html(data=None):
        recipients_list = [data["email"]]
        subject, from_email = "Zlecenie w trakcie realizacji.", settings.SENDER
        text_message = f"Realizujemy zlecenie, czekaj na kolejne wiadomości."

        msg_html = render_to_string("emails/customer_order_in_progress.html", data)
        msg = EmailMultiAlternatives(subject, text_message, from_email, recipients_list)
        msg.attach_alternative(msg_html, "text/html")
        msg.send()

    @staticmethod
    def performer_order_in_progress_html(data=None, url=None):
        data["url"] = url
        subject, from_email = "Zmieniono status zlecenia.", settings.SENDER
        text_message = f"Zmieniłeś status na 'W TRAKCIE REALIZACJI'."

        msg_html = render_to_string("emails/performer_order_in_progress.html", data)
        msg = EmailMultiAlternatives(
            subject, text_message, from_email, settings.PERFORMERS_LIST
        )
        msg.attach_alternative(msg_html, "text/html")
        msg.send()

    @staticmethod
    def customer_order_rejected(data=None):
        recipients_list = [data["email"]]
        subject, from_email = "Zlecenie odrzucone.", settings.SENDER
        text_message = f"Niestety Twoje zlecenie zostało odrzucone."

        msg_html = render_to_string("emails/customer_order_rejected.html", data)
        msg = EmailMultiAlternatives(subject, text_message, from_email, recipients_list)
        msg.attach_alternative(msg_html, "text/html")
        msg.send()

    @staticmethod
    def customer_order_done_with_files(data=None, attachment=None):
        recipients_list = [data["email"]]
        subject, from_email = "Oto Twoje zrealizowane zlecenie.", settings.SENDER
        text_message = f"Zrealizowane zlecenie z plikami."

        msg_html = render_to_string("emails/customer_order_done.html", data)
        msg = EmailMultiAlternatives(subject, text_message, from_email, recipients_list)
        msg.attach_alternative(msg_html, "text/html")
        for i in attachment:
            msg.attach_file(i)
        msg.send()
