from django.shortcuts import redirect, render
from django.http import HttpResponse;
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView

from .forms import StudentRegistrationForm, SkladanieFormularzaDlaNiepelnosprawnych
# Create your views here.

def main(request):
    return HttpResponse("Witam na platformie stypendialnej!")

def loginPage(request):
    return HttpResponse("Strona logowania")

def registerPage(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = StudentRegistrationForm()
    return render(request, 'website/rejestracja.html', {'form': form})

def ZlozenieFormularzaNiepelnosprawnych(request):
    if request.method == 'POST':
        form = SkladanieFormularzaDlaNiepelnosprawnych(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SkladanieFormularzaDlaNiepelnosprawnych()
    return render(request, 'website/form_niepelno.html', {'form': form}) 

class Formularze(TemplateView):
    template_name = 'website/formularze.html'

class Kontakt(TemplateView):
    template_name = 'website/kontakt.html'

class Logowanie(TemplateView):
    template_name = 'website/logowanie.html'