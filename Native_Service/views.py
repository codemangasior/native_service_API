from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.conf import settings
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .models import NativePost
from .forms import PricingForm
from .forms import FinalPricingForm
from .forms import BusinessForm
from .forms import OfficialForm
from .forms import JobHomeCarForm
from .forms import TranslatingForm
from .forms import CustomAuthenticationForm
from Native_Service.lib.native_service import ProgressStages
from Native_Service.lib.native_service import UrlsGenerator
from Native_Service.lib.native_service import SecretKey
import datetime
import json
import urllib
from urllib import parse
from urllib import request


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

        # Gets secret_key from session
        secret_key = self.request.session["secret_key"]

        # Creates empty list prepared for coded files names
        coded_files_list = []

        post = form.save(commit=False)

        # reCAPTCHA validation
        recaptcha_response = self.request.POST.get("g-recaptcha-response")
        url = "https://www.google.com/recaptcha/api/siteverify"
        values = {
            "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            "response": recaptcha_response,
        }
        data = parse.urlencode(values).encode()
        req = request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())

        if result["success"]:
            post.save()

            # Saves files to the path directory
            path = (
                settings.MEDIA_ROOT + f"uploads/{datetime.date.today()}/{secret_key}/"
            )
            for f in self.files:
                fs = FileSystemStorage(location=path)
                # todo needs to better support files without extension
                extension = str(f).rsplit(".")[-1]
                file_name = f"{get_random_string(12)}.{extension}".replace(" ", "")
                coded_files_list.append(file_name)

                # Saves file content as coded filename
                fs.save(file_name, ContentFile(f.read()))

            # Creates custom url for performer
            url = UrlsGenerator().view_finalpricing_url(secret_key)
            # Initializing Progress Stages library
            # Initializing Progress Stages library
            ProgressStages().in_queue_stage(data=form.cleaned_data, url=url)
            # Passing coded_files_list by session to other methods
            self.request.session["coded_files_list"] = coded_files_list

            self.request.session.set_test_cookie()
            return super().form_valid(form)

        else:
            return super().form_invalid(form)


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
            secret_key = self.request.session["secret_key"]

            # Gets coded_files_data from session
            coded_files_data = self.request.session["coded_files_list"]

            # Function gets all data from all models with secret_key
            data_dict = _get_data_from_models(secret_key)

            # coded_files_list >>> coding as JSON and saves in NativePost(current order) database
            json_coded = json.dumps(coded_files_data)
            post = NativePost.objects.get(secret_key=secret_key)
            post.list_files = json_coded
            post.save()

            self.request.session.delete_test_cookie()
            return self.render_to_response(data_dict)
        else:
            raise PermissionError("Cookies Error.")


class FileListView(LoginRequiredMixin, TemplateView):
    """ Special view for logged in performer to can see all files. """

    template_name = "file_list.html"

    def get_context_data(self, **kwargs):
        # Gets 'secret_key' from url
        path = self.request.path
        secret_key = path.rsplit("/")[-2]

        # Function gets all data from all models with secret_key
        context = _get_data_from_models(secret_key)
        url_date = context["url_date"]

        # Decoding JSON file to python list back
        jsondec = json.decoder.JSONDecoder()
        coded_files_list = jsondec.decode(context["list_files"])

        # Builds files urls list
        performer_urls_list = UrlsGenerator().list_order_files_for_filelistview(
            secret_key=secret_key, coded_files_list=coded_files_list, url_date=url_date
        )
        context["performer_urls_list"] = performer_urls_list

        # Render only if secret key exists in db
        if secret_key == _get_data_from_models(secret_key)["secret_key"]:
            return context
        else:
            raise ValueError("SECRET_KEY does not exist.")

    # todo login redirect view
    def get_login_url(self):
        return reverse_lazy("Native_Service:login")


class FinalPricing(UpdateView):
    """ UpdateView for performer to set a price for customer. """

    model = NativePost
    template_name_suffix = "_update_form"
    form_class = FinalPricingForm
    success_url = reverse_lazy("Native_Service:final_pricing_submit")

    def get(self, request, *args, **kwargs):
        self.request.session.set_test_cookie()
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        # Gets 'secret_key' from url
        path = self.request.path
        secret_key = path.rsplit("/")[-2]

        # Creates FileListView url
        file_list_url = UrlsGenerator().view_filelistview_url(secret_key)

        # Passing secret_key by session to other methods
        self.request.session["secret_key"] = secret_key

        # Updates context
        context["file_list_url"] = file_list_url

        # Render only if secret key exists in db
        if secret_key == _get_data_from_models(secret_key)["secret_key"]:
            return self.render_to_response(context)
        else:
            raise ValueError("SECRET_KEY does not exist.")


class FinalPricingSubmit(TemplateView):
    """ Submit view for performer. """

    template_name = "final_pricing_submit.html"

    def get(self, request, *args, **kwargs):
        if self.request.session.test_cookie_worked:

            # Gets secret_key from session
            secret_key = self.request.session["secret_key"]

            # Function gets all data from all models with secret_key
            data_dict = _get_data_from_models(secret_key)

            # Creates url for customer to see price
            email_url = UrlsGenerator().view_priceforcustomer_url(secret_key)

            # Setting stage in Progress Stages library
            ProgressStages().waiting_for_accept(
                data=data_dict, url=email_url, secret_key=secret_key
            )

            context = self.get_context_data(**kwargs)
            self.request.session.delete_test_cookie()
            return self.render_to_response(context)
        else:
            raise PermissionError("Cookies Error.")


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
        price_accept_url = UrlsGenerator().view_priceaccepteddotpay_url(secret_key)
        data_dict.update({"accept_url": price_accept_url})

        return self.render_to_response(data_dict)


class PriceAcceptedDotpay(TemplateView):
    """ View for a customer to use Dotpay. """

    template_name = "price_accepted.html"

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

            ProgressStages().accepted_stage(data=data_dict, secret_key=secret_key)

            # Secret_key authorization
            if secret_key == url_secret_key:
                self.request.session.delete_test_cookie()
                return self.render_to_response(data_dict)
            else:
                raise ValueError(
                    "SECRET_KEY does not exist, or you have problem with cookies."
                )


class PerformerLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
