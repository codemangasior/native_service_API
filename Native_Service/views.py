from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import NativeUpload


def upload_file(request):
    template_name = "index.html"
    if request.method == "POST":
        form = NativeUpload(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect("upload")
    else:
        form = NativeUpload()
    return render(request, template_name, {"form": form})


def check_your_post(request):
    template_name = "upload.html"
    args = {}
    return render(request, template_name, args)
