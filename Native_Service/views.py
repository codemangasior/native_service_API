from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from .models import NativePost
from .forms import NativeUpload
from Native_Service.lib import native_service


def get(request):
    template_name = "index.html"
    if request.method == "POST":
        form = NativeUpload(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            posts = NativePost.objects.all()
            native_service.new_record_alert(posts.values().latest("id"))
            return HttpResponseRedirect("upload")
    else:
        form = NativeUpload()

    return render(request, template_name, {"form": form})


class RecordView(TemplateView):
    """ RecordView needs fix up. """

    template_name = "upload.html"

    def get(self, request):
        posts = NativePost.objects.all()
        args = posts.values().latest("id")
        return render(request, self.template_name, args)
