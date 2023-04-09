from django.urls import path

from .views import start_handler

urlpatterns = [
    path('start/', start_handler),
]
