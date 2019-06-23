from django.core.mail import send_mail
import datetime

# the vars below must be move to django settings, which BTW i don't see in this project :P
# then you just do:
# from django.conf import settings
# settings.HOST_URL
HOST_URL = "https://api.nativeservice.pl"
SENDER = "nativeservice@nativeservice.pl"


def file_list_creating(file_data):
    return [f"{HOST_URL}/{f}\n" for f in file_data]


def performer_queue_alert_email(data, files="No files."):
    recipients_list = [
        "lukasz.gasiorowski92@gmail.com"
    ]  # the same, must be moved to settings

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
        f"{''.join(file_list_creating(files))}"
        f"\n\nTen email został wygenerowany automatycznie. Prosimy o nie odpowiadanie na wiadomość.",
        SENDER,
        recipients_list,
        fail_silently=False,  # are you sure? You wouldn't know it isn't working and your customers are ignored as I don't see any logging.
    )


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
        f"Opis: {data['description']}\n"
        f"{''.join(file_list_creating(files))}"
        f"\n\nTen email został'wygenerowany automatycznie. Prosimy o nie odpowiadanie na wiadomość.",
        SENDER,
        recipients_list,
        fail_silently=False,
    )


print(datetime.date.today())
