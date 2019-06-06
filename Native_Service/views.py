from django.shortcuts import render
from django.views.generic import FormView
from .models import NativePost
from .forms import NativePostForm
from Native_Service.lib.native_service import ProgressStages


class Pricing(FormView):
    """ Pricing view for not logged in users. """

    template_name = "index.html"
    form_class = NativePostForm
    success_url = "/upload"

    def form_valid(self, form):
        """ Form validation with an email alert for NativeService. """
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            # initializing Progress Stages library
            ProgressStages(form.cleaned_data)
            self.request.session["form"] = True

        return super().form_valid(form)


class FormSubmit(Pricing):
    """ Correct form view protected by session. """

    def render_to_response(self, context, **response_kwargs):
        """ Form data rendering in submit view. Protected by session. """
        template_name = "upload.html"
        posts = NativePost.objects.all()
        args = posts.values().last()
        if self.request.session["form"] == True:
            self.request.session["form"] = False
            return render(self.request, template_name, args)
