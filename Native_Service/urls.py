from django.urls import path
from Native_Service.views import upload_file, check_your_post
from django.conf.urls.static import static
from django.conf import settings


app_name = "Native_Service"
urlpatterns = [
    path("", upload_file, name="index"),
    path("upload", check_your_post, name="upload"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
