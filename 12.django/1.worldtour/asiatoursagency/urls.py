from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact_view, name='contact'),
    path('contact/success', views.contact_success_view, name='contact-success'),
    path('home', views.home_view, name='home'),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('protected', views.ProtectedView.as_view(), name='protected'),
]