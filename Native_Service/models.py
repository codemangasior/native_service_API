from django.db import models

# from django.urls import reverse


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

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICE)
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    title = models.CharField(max_length=120)
    priority = models.CharField(
        max_length=15, choices=PRIORITY_CHOICE, default="STANDARD"
    )
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    date_time = models.DateTimeField(auto_now_add=True)
    date_to_be_done = models.DateField()
    description = models.CharField(max_length=1000)
    # todo model shows only one file when more of them are uploaded
    file = models.FileField(null=True, blank=True)
    secret_key = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.name} {self.last_name} tel:{self.phone} key:{self.secret_key}"


class FinalPricing(models.Model):
    time_to_get_ready = models.DateField()
    price = models.CharField(max_length=10)
    comments = models.CharField(max_length=500)
    # todo need to lock situation when secret key is uploaded more than once
    secret_key = models.CharField(max_length=45)

    def __str__(self):
        # todo model needs to get more information from NativePost
        return self.secret_key

    """
    def get_absolute_url(self):
        return reverse("finalpricing", kwargs={"secret_key": self.secret_key})
    """
