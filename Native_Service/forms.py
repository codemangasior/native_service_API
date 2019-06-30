from django import forms
from .models import NativePost


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

class PricingForm(forms.ModelForm):
    """ Basic form for all categories. """

    email = forms.CharField(label="Email", max_length=100, widget=forms.EmailInput())
    date_to_be_done = forms.DateField(
        widget=forms.SelectDateWidget(months=MONTHS),
        label="Data najpóźniejszej realizacji",
    )
    description = forms.CharField(
        label="Opis zlecenia", max_length=1000, widget=forms.Textarea
    )
    file = forms.FileField(
        label="Plik",
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )
    secret_key = forms.CharField(required=True, widget=forms.HiddenInput())
    slug = forms.CharField(required=True, widget=forms.HiddenInput())


    class Meta:
        model = NativePost
        fields = (
            "category",
            "name",
            "last_name",
            "title",
            "priority",
            "email",
            "phone",
            "date_to_be_done",
            "description",
            "file",
            "secret_key",
            "slug",
        )


class BusinessForm(PricingForm):
    category = forms.CharField(max_length=50, initial="REPREZENTOWANIE FIRM", widget=forms.HiddenInput())

    class Meta:
        model = NativePost
        fields = (
            "category",
            "name",
            "last_name",
            "title",
            "priority",
            "email",
            "phone",
            "date_to_be_done",
            "description",
            "file",
            "secret_key",
            "slug",
        )

class OfficialForm(forms.ModelForm):
    pass

class JobHomeCarForm(forms.ModelForm):
    pass

class TranslatingForm(forms.ModelForm):
    pass














class FinalPricingForm(forms.ModelForm):
    """ Performer form to set a price for costumer. """

    time_to_get_ready = forms.DateField(
        widget=forms.SelectDateWidget(months=MONTHS), label="Data planowanej realizacji"
    )
    price = forms.CharField(label="Cena", max_length=10)
    comments = forms.CharField(
        label="Uwagi do wyceny", max_length=500, widget=forms.Textarea
    )
    secret_key = forms.CharField(required=True, widget=forms.HiddenInput())

    class Meta:
        model = NativePost
        fields = ("time_to_get_ready", "price", "comments", "secret_key")
