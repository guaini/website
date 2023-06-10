from django.urls import path

import backend.user as user

urlpatterns = [
    path('User', user.dispatcher),
]
