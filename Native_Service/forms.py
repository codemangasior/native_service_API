from django import forms
from .models import NativePost
import datetime
from django.conf import settings
from django.core.mail import send_mail

MONTHS = {
    1: ("styczeń"),
    2: ("luty"),
    3: ("marzec"),
    4: ("kwiecień"),
    5: ("maj"),
    6: ("czerwiec"),
    7: ("lipiec"),
    8: ("sierpień"),
    9: ("wrzesień"),
    10: ("październik"),
    11: ("listopad"),
    12: ("grudzień"),
}


class NativePostForm(forms.ModelForm):

    name = forms.CharField(label="Imię", max_length=20)
    last_name = forms.CharField(label="Nazwisko", max_length=40)
    title = forms.CharField(label="Nazwa zlecenia", max_length=120)
    email = forms.CharField(label="Email", max_length=100)
    phone = forms.CharField(label="Nr telefonu", max_length=12)
    date_to_be_done = forms.DateField(
        widget=forms.SelectDateWidget(months=MONTHS),
        label="Data najpóźniejszej realizacji",
    )
    description = forms.CharField(
        label="Opis zlecenia", max_length=500, widget=forms.Textarea
    )
    file = forms.FileField(label="Plik", initial="Wybierz plik do zlecenia")

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
