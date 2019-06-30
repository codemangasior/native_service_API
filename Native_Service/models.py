from django.db import models
from django.urls import reverse


# todo create 4 forms based on this model with 4 other views and defaults prefills.
class NativePost(models.Model):

    PRIORITY_CHOICE = [
        ("WYSOKI", "WYSOKI"),
        ("STANDARD", "STANDARD"),
        ("NISKI", "NISKI"),
    ]
    CATEGORY_CHOICE = [
        ("REPREZENTOWANIE FIRM", "REPREZENTOWANIE FIRM"),
        ("SPRAWY URZĘDOWE", "SPRAWY URZĘDOWE"),
        ("PRACA MIESZKANIE AUTO", "PRACA MIESZKANIE AUTO"),
        ("TŁUMACZENIA", "TŁUMACZENIA"),
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
    email = models.CharField(max_length=100, verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Numer Telefonu")
    date_time = models.DateTimeField(auto_now_add=True)
    date_to_be_done = models.DateField()
    description = models.TextField(verbose_name="Opis zlecenia")
    # todo model shows only one file when more of them are uploaded
    secret_key = models.CharField(max_length=45)
    file = models.FileField(upload_to="uploads/%Y/%m/%d/", null=True)
    slug = models.SlugField(unique=True)
    time_to_get_ready = models.DateField(
        verbose_name="Szacowany czas realizacji zlecenia", null=True
    )
    price = models.CharField(max_length=10, verbose_name="Cena", null=True)
    comments = models.TextField(verbose_name="Komentarz do zlecenia", null=True)

    def __str__(self):
        return f"{self.name} {self.last_name} tel:{self.phone} key:{self.secret_key}"

    def get_absolute_url(self):
        return reverse("test", kwargs={"slug": self.secret_key})

    """
    def get_absolute_url(self):
        return reverse("finalpricing", kwargs={"secret_key": self.secret_key})
    """
