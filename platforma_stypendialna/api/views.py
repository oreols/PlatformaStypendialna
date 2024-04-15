from django.shortcuts import redirect, render
from django.http import HttpResponse;
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .authbackend import CustomAuthBackend

from .forms import StudentRegistrationForm, SkladanieFormularzaDlaNiepelnosprawnych
# Create your views here.

def main(request):
    return HttpResponse("Witam na platformie stypendialnej!")

def loginPage(request):
    if request.method == 'POST':
        nazwa_uzytkownika = request.POST['nazwa_uzytkownika']
        password = request.POST['password']

        user = CustomAuthBackend().authenticate(request, username=nazwa_uzytkownika, password=password)

        if user is not None:
            user.backend = 'django.authbackend.CustomAuthBackend'
            login(request, user)
            return HttpResponse("Zalogowano")
        else:
            return HttpResponse("Nieprawidłowa nazwa użytkownika lub hasło")
        
    return render(request, 'website/logowanie.html')

def registerPage(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            nazwa_uzytkownika = request.POST['nazwa_uzytkownika']
            password = request.POST['password']
            form.instance.password = make_password(password)
            form.save()
    else:
        form = StudentRegistrationForm()
    return render(request, 'website/rejestracja.html', {'form': form})

def ZlozenieFormularzaNiepelnosprawnych(request):
    if request.method == 'POST':
        form = SkladanieFormularzaDlaNiepelnosprawnych(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = SkladanieFormularzaDlaNiepelnosprawnych()
    return render(request, 'website/form_niepelno.html', {'form': form}) 
    redirect('website/kontakt.html')

class Formularze(TemplateView):
    template_name = 'website/formularze.html'

class Kontakt(TemplateView):
    template_name = 'website/kontakt.html'

class Logowanie(TemplateView):
    template_name = 'website/logowanie.html'