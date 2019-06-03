from django import forms
from .models import NativePost
import datetime


class NativeUpload(forms.ModelForm):

    title = forms.CharField(label="Nazwa zlecenia", max_length=120)
    email = forms.CharField(label="Email", max_length=100)
    phone = forms.CharField(label="Nr telefonu", max_length=12)
    date_to_be_done = forms.DateTimeField(
        label="Data realizacji zlecenia:", initial=datetime.date.today
    )
    description = forms.CharField(label="Opis zlecenia", max_length=500)
    file = forms.FileField(label="Plik")

    class Meta:
        model = NativePost
        fields = ("title", "email", "phone", "date_to_be_done", "description", "file")
