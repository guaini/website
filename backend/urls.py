from django.urls import path

import backend.picture as picture
import backend.user as user

urlpatterns = [
    path('User', user.dispatcher),
    path('Picture', picture.dispatcher),
]
