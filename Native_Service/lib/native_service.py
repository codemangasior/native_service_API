import os
from django.core.mail import send_mail
from django.conf import settings

os.environ["DJANGO_SETTINGS_MODULE"] = "Native_Service.settings_module"


def new_record_alert(data):
    send_mail(
        f"Nowe zlecenie!",
        f"Wejdź na https://nativeservice.pl/admin/ i sprawdź co na Ciebie czeka.\n"
        f"Zlecenie nr: {data['id']}\n"
        f"Imię: {data['name']}\n"
        f"Nazwisko: {data['last_name']}\n"
        f"Nazwa zlecenia: {data['title']}\n"
        f"Email: {data['email']}\n"
        f"Telefon: {data['phone']}\n"
        f"Data napóźniejszej realizacji {data['date_to_be_done']}\n"
        f"Opis: {data['description']}\n"
        f"Plik: https://api.nativeservice.pl{settings.MEDIA_URL}{data['file']}",
        "lukasz.gasiorowski92@gmail.com",
        ["lukasz.gasiorowski92@gmail.com"],
        fail_silently=False,
    )
