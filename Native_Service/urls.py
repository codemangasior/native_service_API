from django.urls import path
from Native_Service import views
from django.conf.urls.static import static
from django.conf import settings


app_name = "Native_Service"
urlpatterns = [
    path("", views.Pricing.as_view(), name="index"),
    path("upload", views.FormSubmit.as_view(), name="upload"), # it's a wrong name, you don't upload anything here, it's a success page
    path(
        "confrimation/<int:pk>", views.EmailComfirmation.as_view(), name="confirmation"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
