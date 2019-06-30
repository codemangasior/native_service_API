from django.urls import path
from Native_Service import views
from django.conf.urls.static import static
from django.conf import settings


app_name = "Native_Service"
urlpatterns = [
    path("", views.IndexCategorySelect.as_view(), name="index"),
    path("pricing", views.Pricing.as_view(), name="pricing"),
    path("pricing_submit", views.SubmitPricing.as_view(), name="submit_pricing"),
    path(
        "final_pricing/<slug:slug>/", views.FinalPricing.as_view(), name="final_pricing"
    ),
    path(
        "final_pricing_submit/",
        views.FinalPricingSubmit.as_view(),
        name="final_pricing_submit",
    ),
    path(
        "price_for_you/<slug:slug>/",
        views.PriceForCustomer.as_view(),
        name="price_for_you",
    ),
    path(
        "price_accepted/<slug:slug>/",
        views.PriceAcceptedDotpay.as_view(),
        name="price_accepted",
    ),
    path("business_form", views.BusinessFormView.as_view(), name="business_form"),
    path("official_form", views.OfficialFormView.as_view(), name="official_form"),
    path("jobhomecar_form", views.JobHomeCarFormView.as_view(), name="jobhomecar_form"),
    path(
        "translating_form", views.TranslatingFormView.as_view(), name="translating_form"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

