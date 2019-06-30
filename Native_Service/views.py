from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.conf import settings
from django.views.generic import FormView, TemplateView, UpdateView
from django.shortcuts import render
from .models import NativePost
from .forms import PricingForm
from .forms import FinalPricingForm
from Native_Service.lib.native_service import ProgressStages
from Native_Service.lib.native_service import UrlsGenerator
from Native_Service.lib.native_service import SecretKey
import datetime

# todo Views need to return 404 errors while any bugs appear

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

    template_name = "pricing.html"
    success_url = "/pricing_submit"
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

    def post(self, request, *args, **kwargs):
        """Method posts form and saves the files in storage """
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # Makes list of files
        self.files = request.FILES.getlist("file")
        
        if form.is_valid():
            path = settings.MEDIA_ROOT + f"uploads/{datetime.date.today()}/"
            for f in self.files:

                fs = FileSystemStorage(location=path)
                fs.save(f"{f}".replace(" ", "_"), ContentFile(f.read()))

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """ Form validation with an email alert for NativeService. """

        # Gets secret_key from session
        secret_key = self.request.session["secret_key"]
        post = form.save(commit=False)
        #print(self.request.FILES.path)
        post.save()


        # Creates custom url for performer
        url = UrlsGenerator().final_pricing_url_genrator(secret_key)
        # Initializing Progress Stages library
        ProgressStages(form.cleaned_data, self.files, url).in_queue_stage()

        self.request.session.set_test_cookie()
        return super().form_valid(form)


class SubmitPricing(Pricing):
    """ Correct form view for CUSTOMER protected by session. """

    def get(self, request, *args, **kwargs):
        if self.request.session.test_cookie_worked():
            # Gets secret_key from session
            self.secret_key = self.request.session["secret_key"]
            return self.render_to_response(self.get_context_data())

    def render_to_response(self, context, **response_kwargs):
        """ Form data rendering in submit view. Protected by session. """
        template_name = "pricing_submit.html"

        if self.request.session.test_cookie_worked():
            # Function gets all data from all models with secret_key
            data_dict = _get_data_from_models(self.secret_key)

            self.request.session.delete_test_cookie()
            return render(self.request, template_name, data_dict)


class FinalPricing(UpdateView):
    """ UpdateView for performer to set a price for customer. """

    model = NativePost
    #fields = ['price', 'comments', 'time_to_get_ready']
    template_name_suffix = '_update_form'
    success_url = "final-pricing-submit"
    form_class = FinalPricingForm

    def get(self, request, *args, **kwargs):
        # Gets 'secret_key' from url
        path = self.request.path
        secret_key = path.rsplit("/")[-2]

        # Passing secret_key by session to other methods
        self.request.session["secret_key"] = secret_key

        # Render only if secret key exists in db
        if secret_key == _get_data_from_models(secret_key)["secret_key"]:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        self.request.session.set_test_cookie()
        return super().post(request, *args, **kwargs)


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

            # Creates url which gives possibility to accept price by customer
            price_accept_url = UrlsGenerator().accept_price_url_generator(secret_key)

            # Setting stage in Progress Stages library      #todo \/ redundant now IMO
            ProgressStages(
                data=data_dict, url=email_url, url_accept_price=price_accept_url
            ).pricing_in_progress_stage()

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
    #todo email alert for performer about waiting for payment
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
