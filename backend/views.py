from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json
import jwt
import time

from jwt import ExpiredSignatureError

from backend.models import User, Picture, Favorite, Tag, PictoTag


# Create your views here.
def index(request):
    return render(request, 'index.html')


def detail(request):
    return render(request, 'detail.html')


def to_login(request):
    return render(request, 'login.html')


def to_set(request):
    return render(request, 'set.html')


def to_star(request):
    return render(request, 'star.html')


def to_upload(request):
    return render(request, 'upload.html')
