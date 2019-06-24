from django.urls import path
from Native_Service import views
from django.conf.urls.static import static
from django.conf import settings


app_name = "Native_Service"
urlpatterns = [
    path("", views.IndexCategorySelect.as_view(), name="index"),
    path("pricing", views.Pricing.as_view(), name="pricing"),
    path("upload", views.SubmitPricing.as_view(), name="submit_pricing"),
    path(
        "final_pricing/<str:secret_key>/",
        views.FinalPricing.as_view(),
        name="final_pricing",
    ),
    path(
        "final_pricing/<str:secret_key>/final_pricing_submit/",
        views.FinalPricingSubmit.as_view(),
        name="final_pricing_submit",
    ),
    path(
        "price_for_you/<str:secret_key>/",
        views.PriceForCustomer.as_view(),
        name="price_for_you",
    ),
    path(
        "price_accepted/<str:secret_key>/",
        views.PriceAcceptedDotpay.as_view(),
        name="price_accepted",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
