from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('contact', views.contact_view, name='contact'),
    path('contact/success', views.contact_success_view, name='contact-success'),
]