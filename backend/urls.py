from django.urls import path
import backend.user as user
import backend.picture as picture
import backend.index as index
import backend.views as views

urlpatterns = [
    path('User', user.dispatcher),
    path('Picture/upload', views.upload),
    path('Picture', picture.dispatcher),
    path('Index', index.dispatcher),
]
