from django import forms
from .models import NativePost
import datetime
from django.forms import widgets


class NativeUpload(forms.ModelForm):

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
