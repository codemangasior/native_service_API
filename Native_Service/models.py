from django.db import models
from django.urls import reverse



class NativePost(models.Model):
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    title = models.CharField(max_length=120)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    date = models.DateTimeField(auto_now_add=True)
    date_to_be_done = models.DateTimeField()
    description = models.CharField(max_length=500)
    file = models.FileField(upload_to="uploads/%Y/%m/%d/", null=True, blank=True)

    def __str__(self):
        return self.title
