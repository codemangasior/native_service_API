from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from .models import NativePost
from .forms import NativePostForm
from Native_Service.lib.native_service import ProgressStages, secret_key_generator
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.conf import settings
import datetime


"""
def dispatch(self, request, *args, **kwargs):
    import pdb # you don't need to import pdb if you're using `breakpoint()`
    breakpoint()
    return super().dispatch(request, *args, **kwargs)
"""


class Pricing(FormView):
    """ Pricing view for not logged in users. """

    template_name = "index.html"
    secret_key = None
    form_class = NativePostForm
    success_url = (
        "/upload"
    )  # instead of using plain url, use django's `reverse` function and pass the name of the upload view.
    files = None

    def get(self, request, *args, **kwargs):
        """ Method generates secret_key in every request. """
        self.secret_key = secret_key_generator()
        # Sets secret_key as default value in form.
        self.initial = {"secret_key": self.secret_key}
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # I think you can move this whole file hanling code to `form_valid`. Also the contidion `form.is_valid()` is handled by FormView itself.
        self.files = request.FILES.getlist("file")
        if form.is_valid():
            # use FileField instead, it does it all for you, including the file name generating
            # look at the example https://docs.djangoproject.com/en/2.2/ref/models/fields/#filefield
            # upload = models.FileField(upload_to='uploads/%Y/%m/%d/')
            for f in self.files:
                fs = FileSystemStorage(
                    location=settings.MEDIA_ROOT + f"uploads/{datetime.date.today()}/"
                )
                fs.save(f"{f}", ContentFile(f.read()))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """ Form validation with an email alert for NativeService. """
        post = form.save(commit=False)
        post.save()
        # initializing Progress Stages library
        # you should not implicilty do any action in `__init__` method. Instead, create and object, and execute `in_queue_stage` exlicitely in the next line. Also think about better name. This one does not tell me that i'm sending emials by executing it :P So make it that it tells me what it does.
        ProgressStages(form.cleaned_data, self.files)
        self.request.session.set_test_cookie()
        return super().form_valid(form)


class FormSubmit(Pricing):
    # You should:
    # - use `Pricing` view as the view for subbmiting forms
    # - do not inherit from Pricing, as you're not handling any form here, it's just a success page view.
    """ Correct form view protected by session. """

    def render_to_response(self, context, **response_kwargs):
        """ Form data rendering in submit view. Protected by session. """
        template_name = "upload.html"
        posts = NativePost.objects.all()
        args = (
            posts.values().last()
        )  # you cannot assume that the last post was done by the person with this cookie. You need to assign the `pk` of the `NativePost` in previous view to some variable in session, and here get this variable's value, and use this `pk` to search for the proper post. PTAL: https://docs.djangoproject.com/en/2.2/topics/http/sessions/#examples
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return render(self.request, template_name, args)


class EmailComfirmation(TemplateView):
    template_name = "email_comfirmation.html"
