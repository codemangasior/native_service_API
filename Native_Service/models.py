from django.db import models


class NativePost(models.Model):

    CATEGORY_CHOICE = [
        ("REPREZENTOWANIE FIRM", "REPREZENTOWANIE FIRM"),
        ("SPRAWY URZĘDOWE", "SPRAWY URZĘDOWE"),
        ("PRACA MIESZKANIE AUTO", "PRACA MIESZKANIE AUTO"),
        ("TŁUMACZENIA", "TŁUMACZENIA"),
    ]
    PRIORITY_CHOICE = [
        ("WYSOKI", "WYSOKI"),
        ("STANDARD", "STANDARD"),
        ("NISKI", "NISKI"),
    ]
    STAGE = [
        ("W KOLEJCE", "W KOLEJCE"),
        ("OCZEKIWANIE NA AKCEPTACJĘ", "OCZEKIWANIE NA AKCEPTACJĘ"),
        ("ZAAKCEPTOWANE", "ZAAKCEPTOWANE"),
        ("OPŁACONE", "OPŁACONE"),
        ("W TRAKCIE REALIZACJI", "W TRAKCIE REALIZACJI"),
        ("ZAKOŃCZONE", "ZAKOŃCZONE"),
        ("ODRZUCONE", "ODRZUCONE"),
    ]

    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICE, verbose_name="Kategoria"
    )
    name = models.CharField(max_length=50, verbose_name="Imię")
    last_name = models.CharField(max_length=50, verbose_name="Nazwisko")
    title = models.CharField(max_length=200, verbose_name="Nazwa zlecenia")
    priority = models.CharField(
        max_length=15,
        choices=PRIORITY_CHOICE,
        default="STANDARD",
        verbose_name="Priorytet",
    )
    stage = models.CharField(
        max_length=50, choices=STAGE, default="W KOLEJCE", verbose_name="Etap zlecenia"
    )
    email = models.CharField(max_length=100, verbose_name="Twój e-mail")
    phone = models.CharField(max_length=20, verbose_name="Twój numer Telefonu")
    url_date = models.DateField(auto_now_add=True)
    create = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    date_to_be_done = models.DateField(verbose_name="Data najpóźniejszej realizacji")
    description = models.TextField(verbose_name="Opis zlecenia")
    secret_key = models.CharField(max_length=45)
    slug = models.SlugField(unique=True)
    time_to_get_ready = models.DateField(
        verbose_name="Szacowany czas realizacji zlecenia", null=True
    )
    price = models.IntegerField(verbose_name="Cena", null=True)
    comments = models.TextField(verbose_name="Komentarz do zlecenia", null=True)
    file = models.CharField(null=True, blank=True, verbose_name="Plik", max_length=255)
    list_files = models.TextField(null=True, blank=True, verbose_name="Lista")

    def __str__(self):
        return f"{self.name} {self.last_name} tel:{self.phone} key:{self.secret_key}"


class NativeProduct(models.Model):
    nativepost = models.ForeignKey(
        NativePost,
        on_delete=models.CASCADE,
        related_name="product",
        null=True,
        blank=True,
    )
    information = models.TextField(
        null=True, blank=True, verbose_name="Informacja końcowa"
    )
    attachments = models.CharField(
        null=True, blank=True, verbose_name="Załączniki", max_length=255
    )
