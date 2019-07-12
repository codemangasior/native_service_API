from .models import NativePost
from .models import NativeProduct
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


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
    # todo validation for doc, docx, pdf, txt, png, jpeg, jpg, webp
    # todo set size limits
    file = forms.FileField(
        label="Plik",
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )
    secret_key = forms.CharField(required=True, widget=forms.HiddenInput())
    slug = forms.CharField(required=True, widget=forms.HiddenInput())
    stage = forms.CharField(initial="W KOLEJCE", widget=forms.HiddenInput())

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
            "file",
            "stage",
        )


class BusinessForm(PricingForm):
    """ Basic form with the predefined category. """

    category = forms.CharField(
        max_length=50, initial="REPREZENTOWANIE FIRM", widget=forms.HiddenInput()
    )


class OfficialForm(PricingForm):
    """ Basic form with the predefined category. """

    category = forms.CharField(
        max_length=50, initial="SPRAWY URZĘDOWE", widget=forms.HiddenInput()
    )


class JobHomeCarForm(PricingForm):
    """ Basic form with the predefined category. """

    category = forms.CharField(
        max_length=50, initial="PRACA MIESZKANIE AUTO", widget=forms.HiddenInput()
    )


class TranslatingForm(PricingForm):
    """ Basic form with the predefined category. """

    category = forms.CharField(
        max_length=50, initial="TŁUMACZENIA", widget=forms.HiddenInput()
    )


class FinalPricingForm(forms.ModelForm):
    """ Performer form to set a price for costumer. """

    time_to_get_ready = forms.DateField(
        widget=forms.SelectDateWidget(months=MONTHS), label="Data planowanej realizacji"
    )
    price = forms.CharField(label="Cena [zł]", max_length=10)
    comments = forms.CharField(
        label="Uwagi do wyceny", max_length=500, widget=forms.Textarea
    )
    secret_key = forms.CharField(required=True, widget=forms.HiddenInput())

    class Meta:
        model = NativePost
        fields = ("time_to_get_ready", "price", "comments", "secret_key")


class RejectOrderForm(forms.ModelForm):
    """ Performer form to reject order. """

    comments = forms.CharField(
        label="Przyczyna odrzucenia", max_length=500, widget=forms.Textarea
    )
    secret_key = forms.CharField(required=True, widget=forms.HiddenInput())

    class Meta:
        model = NativePost
        fields = ("comments", "secret_key")


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label="Użytkownik", widget=forms.TextInput(attrs={"autofocus": True})
    )
    password = forms.CharField(label="Hasło", strip=False, widget=forms.PasswordInput)


class ProductForm(forms.ModelForm):
    attachments = forms.FileField(
        label="Załączniki",
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )

    class Meta:
        model = NativeProduct
        fields = ("information", "attachments")
