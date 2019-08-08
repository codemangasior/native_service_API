from django.urls import path
from django.conf import settings
from django.conf.urls import re_path
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from Native_Service import views


@login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)


app_name = "Native_Service"
urlpatterns = [
    path("", views.IndexCategorySelect.as_view(), name="index"),
    path("pricing", views.Pricing.as_view(), name="pricing"),
    path("business_form", views.BusinessFormView.as_view(), name="business_form"),
    path("official_form", views.OfficialFormView.as_view(), name="official_form"),
    path("jobhomecar_form", views.JobHomeCarFormView.as_view(), name="jobhomecar_form"),
    path(
        "translating_form", views.TranslatingFormView.as_view(), name="translating_form"
    ),
    path("pricing_submit", views.SubmitPricing.as_view(), name="submit_pricing"),
    path(
        "final_pricing/<slug:slug>/", views.FinalPricing.as_view(), name="final_pricing"
    ),
    path("file_list/<slug:slug>/", views.FileListView.as_view(), name="file_list"),
    path(
        "final_pricing_submit/",
        views.FinalPricingSubmit.as_view(),
        name="final_pricing_submit",
    ),
    path(
        "price_for_you/<slug:slug>/",
        views.PriceForCustomer2.as_view(),
        name="price_for_you",
    ),
    path(
        "price_accepted/<slug:slug>/",
        views.PriceAcceptedDotpay.as_view(),
        name="price_accepted",
    ),
    path(
        "successful_payment/<slug:slug>/",
        views.SuccessfulPayment.as_view(),
        name="successful_payment",
    ),
    path("notify/<slug:slug>/", views.notify, name="notifyt"),
    path(
        "in_progress/<slug:slug>/",
        views.OrderInProgress.as_view(),
        name="order_in_progress",
    ),
    path("reject_order/<slug:slug>/", views.RejectOrder.as_view(), name="reject_order"),
    path(
        "reject_order_submit/",
        views.RejectOrderSubmit.as_view(),
        name="reject_order_submit",
    ),
    path("order_done/<slug:slug>/", views.OrderDone.as_view(), name="order_done"),
    path(
        "order_done_submit/", views.OrderDoneSubmit.as_view(), name="order_done_submit"
    ),
    re_path(
        r"^%s(?P<path>.*)$" % settings.MEDIA_URL[1:],
        protected_serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
    path("login", views.PerformerLoginView.as_view(), name="login"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
