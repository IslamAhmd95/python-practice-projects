import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from .form import LoginForm, RegisterForm

from .models import Tour
from .form import ContactForm


# Create your views here.
def index(request):
    tours = Tour.objects.all()
    context = {'tours': tours}
    return render(request, 'tours/index.html', context)


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_email()
            return redirect('contact-success')
    else:
        form = ContactForm()
    return render(request, 'contact/index.html', {'form': form})


def contact_success_view(request):
    return render(request, 'contact/contact_success.html')


@login_required
def home_view(request):
    return render(request, 'auth/home.html')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):

    context = {}
    next_url = request.POST.get('next') or request.GET.get('next') or 'home'

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url)
            else:
                context['error'] = "Invalid credentials!"
    else:
        form = LoginForm()
    
    context['form'] = form
    context['next'] = next_url
    return render(request, 'auth/login.html', context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return redirect('home')

    
class ProtectedView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'auth/protected.html')