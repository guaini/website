from django.urls import path

import backend.picture as picture
import backend.user as user
import backend.views as views

urlpatterns = [
    path('User', user.dispatcher),
    path('Picture/upload', views.upload),
    path('Picture', picture.dispatcher),
]
