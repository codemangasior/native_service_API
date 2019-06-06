from django import forms
from .models import NativePost
import datetime
from django.conf import settings
from django.core.mail import send_mail



class NativePostForm(forms.ModelForm):

    name = forms.CharField(label="Imię", max_length=20)
    last_name = forms.CharField(label="Nazwisko", max_length=40)
    title = forms.CharField(label="Nazwa zlecenia", max_length=120)
    email = forms.CharField(label="Email", max_length=100)
    phone = forms.CharField(label="Nr telefonu", max_length=12)
    date_to_be_done = forms.DateTimeField(
        label="Data realizacji zlecenia:", initial=datetime.date.today, widget=""
    )
    description = forms.CharField(label="Opis zlecenia", max_length=500)
    file = forms.FileField(label="Plik", initial="Wybierz plik do zlecenia")

    def alert_send_email(self):
        send_mail(
            f"Nowe zlecenie!",
            f"Wejdź na https://nativeservice.pl/admin/ i sprawdź co na Ciebie czeka.\n"
            f"Imię: {self.cleaned_data['name']}\n"
            f"Nazwisko: {self.cleaned_data['last_name']}\n"
            f"Nazwa zlecenia: {self.cleaned_data['title']}\n"
            f"Email: {self.cleaned_data['email']}\n"
            f"Telefon: {self.cleaned_data['phone']}\n"
            f"Data napóźniejszej realizacji {self.cleaned_data['date_to_be_done']}\n"
            f"Opis: {self.cleaned_data['description']}\n"
            f"Plik: https://api.nativeservice.pl{settings.MEDIA_URL}{self.cleaned_data['file']}",
            "tlumaczenia@nativeservice.pl",
            ["lukasz.gasiorowski92@gmail.com"],
            fail_silently=False,
        )

    class Meta:
        model = NativePost
        fields = (
            "name",
            "last_name",
            "title",
            "email",
            "phone",
            "date_to_be_done",
            "description",
            "file",
        )
