from django import forms
from .models import NativePost

# unnecessary parenthesis
MONTHS = {
    1: "styczeń",
    2: "luty",
    3: "marzec",
    4: "kwiecień",
    5: "maj",
    6: "czerwiec",
    7: "lipiec",
    8: "sierpień",
    9: "wrzesień",
    10: "październik",
    11: "listopad",
    12: "grudzień",
}


class NativePostForm(forms.ModelForm):
    # The main ModelForm feature is that it discovers what fields the Model has and
    # creates inputs for them *automatically*. You don't need to rewrite them all, it's
    # enough to put them in the `Meta.fields` tuple.
    # You write down only the field that you want to override with other than the django
    # default widget, like this `multiple` in file OR when you want to add aditional fields.
    name = forms.CharField(label="Imię", max_length=20)
    last_name = forms.CharField(label="Nazwisko", max_length=40)
    title = forms.CharField(label="Nazwa zlecenia", max_length=120)
    email = forms.CharField(label="Email", max_length=100, widget=forms.EmailInput())
    phone = forms.CharField(label="Nr telefonu", max_length=12)
    date_to_be_done = forms.DateField(
        widget=forms.SelectDateWidget(months=MONTHS),
        label="Data najpóźniejszej realizacji",
    )
    description = forms.CharField(
        label="Opis zlecenia", max_length=500, widget=forms.Textarea
    )
    file = forms.FileField(
        label="Plik", widget=forms.ClearableFileInput(attrs={"multiple": True})
    )
    secret_key = forms.CharField(required=True, widget=forms.HiddenInput())

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
            "secret_key",
        )
