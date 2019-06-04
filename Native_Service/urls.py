from django.urls import path
from Native_Service import views
from django.conf.urls.static import static
from django.conf import settings


app_name = "Native_Service"
urlpatterns = [
    path("", views.get, name="index"),
    path("upload", views.RecordView.as_view(), name="upload"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
