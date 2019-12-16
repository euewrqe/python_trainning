from django.shortcuts import render,HttpResponse
from app01 import models
import os
from django.conf import settings
import subprocess
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import CreateView


# Create your views here.
# class IndexView(View):
#     def get(self, request):
#         return render(request, "index.html")

class IndexView(TemplateView):
    template_name = "index.html"
    def get(self, request, *args, **kwargs):
        return super(IndexView, self).get(request, *args, **kwargs)

class MyCreateView(CreateView):
    template_name_field = {"username": "a123", "password": "b123"}
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        self.object = "UserModel"
        return super(MyCreateView, self).get(request, *args, **kwargs)