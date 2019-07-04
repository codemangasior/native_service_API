from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.conf import settings
from django.views.generic import FormView, TemplateView, UpdateView
from .models import NativePost
from .forms import PricingForm
from .forms import FinalPricingForm
from .forms import BusinessForm
from .forms import OfficialForm
from .forms import JobHomeCarForm
from .forms import TranslatingForm
from Native_Service.lib.native_service import ProgressStages
from Native_Service.lib.native_service import UrlsGenerator
from Native_Service.lib.native_service import SecretKey
import datetime
from django.urls import reverse_lazy


"""
def dispatch(self, request, *args, **kwargs):
    breakpoint()
    return super().dispatch(request, *args, **kwargs)
"""


def _get_data_from_models(secret_key):
    """ Function returns all data filtered with secret_key as a dict."""
    data = NativePost.objects.filter(secret_key=secret_key)

    data_dict = {}
    for i in data.values():
        data_dict.update(i)
    return data_dict


class IndexCategorySelect(TemplateView):
    template_name = "index.html"


class Pricing(FormView):
    """ Pricing view for not logged in users. """

    # formset = inlineformset_factory(UploadedFile, NativePost, fields=("file",), extra=1)

    template_name = "pricing.html"
    success_url = reverse_lazy("Native_Service:submit_pricing")
    form_class = PricingForm
    secret_key = None
    files = None

    def get(self, request, *args, **kwargs):
        """ Method generates secret_key in every request. """
        secret_key = SecretKey().create()

        # Passing secret_key by session to other methods
        self.request.session["secret_key"] = secret_key

        # Sets secret_key as default value in form.
        self.initial = {"secret_key": secret_key, "slug": secret_key}
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        """ Form validation with an email alert, and files support for NativeService. """

        # Makes list of files
        self.files = self.request.FILES.getlist("file")

        # Saves files to the path directory
        server_patch = f"uploads/{datetime.date.today()}/"
        path = settings.MEDIA_ROOT + server_patch
        for f in self.files:
            fs = FileSystemStorage(location=path)
            fs.save(f"{f}".replace(" ", "_"), ContentFile(f.read()))

        # Gets secret_key from session
        secret_key = self.request.session["secret_key"]
        post = form.save(commit=False)
        post.save()

        # Creates custom url for performer
        url = UrlsGenerator().final_pricing_url_genrator(secret_key)
        # Initializing Progress Stages library
        ProgressStages().in_queue_stage(
            data=form.cleaned_data, files=self.files, url=url
        )

        self.request.session.set_test_cookie()
        return super().form_valid(form)


class BusinessFormView(Pricing):
    """ Business category view. """

    template_name = "business_form.html"
    form_class = BusinessForm


class OfficialFormView(Pricing):
    """ Official category view. """

    template_name = "official_form.html"
    form_class = OfficialForm


class JobHomeCarFormView(Pricing):
    """ Job Home Car category view. """

    template_name = "jobhomecar_form.html"
    form_class = JobHomeCarForm


class TranslatingFormView(Pricing):
    """ Translating category view. """

    template_name = "translating_form.html"
    form_class = TranslatingForm


class SubmitPricing(TemplateView):
    """ Correct form view for CUSTOMER protected by session. """

    template_name = "pricing_submit.html"

    def get(self, request, *args, **kwargs):
        """ Form data rendering in submit view. Protected by session. """

        if self.request.session.test_cookie_worked():
            # Gets secret_key from session
            self.secret_key = self.request.session["secret_key"]

            # Function gets all data from all models with secret_key
            data_dict = _get_data_from_models(self.secret_key)

            self.request.session.delete_test_cookie()
            return self.render_to_response(data_dict)


class FinalPricing(UpdateView):
    """ UpdateView for performer to set a price for customer. """

    model = NativePost
    template_name_suffix = "_update_form"
    form_class = FinalPricingForm
    success_url = reverse_lazy("Native_Service:final_pricing_submit")

    def get(self, request, *args, **kwargs):
        self.request.session.set_test_cookie()

        # Gets 'secret_key' from url
        path = self.request.path
        secret_key = path.rsplit("/")[-2]
        self.some = secret_key

        # Passing secret_key by session to other methods
        self.request.session["secret_key"] = secret_key

        # Render only if secret key exists in db
        if secret_key == _get_data_from_models(secret_key)["secret_key"]:
            return super().get(request, *args, **kwargs)


class FinalPricingSubmit(TemplateView):
    """ Simple form submit view. """

    template_name = "final_pricing_submit.html"

    def get(self, request, *args, **kwargs):
        if self.request.session.test_cookie_worked:

            # Gets secret_key from session
            secret_key = self.request.session["secret_key"]

            # Function gets all data from all models with secret_key
            data_dict = _get_data_from_models(secret_key)

            # Creates url for customer to see price
            email_url = UrlsGenerator().accept_view_url_generator(secret_key)

            # Setting stage in Progress Stages library
            ProgressStages().pricing_in_progress_stage(data=data_dict, url=email_url)

            context = self.get_context_data(**kwargs)
            self.request.session.delete_test_cookie()
            return self.render_to_response(context)


class PriceForCustomer(TemplateView):
    """ View for a customer which gives the possibility to accept the price. """

    template_name = "price_for_you.html"

    def get(self, request, *args, **kwargs):
        self.request.session.set_test_cookie()

        # Gets 'secret_key' from url
        path = self.request.path
        secret_key = path.rsplit("/")[-2]

        # Passing secret key with session to next view
        self.request.session["secret_key"] = secret_key

        # Function gets all data from all models with secret_key
        data_dict = _get_data_from_models(secret_key)

        # Creates url which gives possibility to accept price by customer
        price_accept_url = UrlsGenerator().accept_price_url_generator(secret_key)
        data_dict.update({"accept_url": price_accept_url})

        return self.render_to_response(data_dict)


class PriceAcceptedDotpay(TemplateView):
    template_name = "price_accepted.html"
    """ View for a customer to use Dotpay. """
    # todo email alert for performer about waiting for payment
    def get(self, request, *args, **kwargs):
        if self.request.session.test_cookie_worked():
            # Gets secret_key from session
            secret_key = self.request.session["secret_key"]
            # Function gets all data from all models with secret_key
            data_dict = _get_data_from_models(secret_key)

            # Gets 'secret_key' from url
            path = self.request.path
            url_secret_key = path.rsplit("/")[-2]

            # Secret_key authorization
            if secret_key == url_secret_key:
                self.request.session.delete_test_cookie()
                return self.render_to_response(data_dict)
