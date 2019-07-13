from django.contrib import admin
from .models import NativePost, NativeProduct

admin.register(admin)
admin.site.register(NativePost)
admin.site.register(NativeProduct)
