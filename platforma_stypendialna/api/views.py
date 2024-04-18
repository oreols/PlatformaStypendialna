from django.shortcuts import redirect, render
from django.http import HttpResponse;
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .authbackend import CustomAuthBackend
from .models import Student, Formularz

from .forms import StudentRegistrationForm, SkladanieFormularzaDlaNiepelnosprawnych
# Create your views here.

def main(request):
    return HttpResponse("Wita platforma stypendialna")

def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse("Zalogowano")
        else:
            return HttpResponse("Nieprawidłowa nazwa użytkownika lub hasło")
        
    return render(request, 'website/logowanie.html')

def registerPage(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            form.instance.password = make_password(password)
            form.save()
            
            return render(request, 'website/logowanie.html', {'form': form})
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

def PanelAdmina(request):
    student = Student.objects.all()
    formularz = Formularz.objects.all()
    context = {'student': student , 'formularz': formularz}
    return render(request, 'website/admin_tables.html', context)

class Formularze(TemplateView):
    template_name = 'website/formularze.html'

class StronaGlowna(TemplateView):
    template_name = 'website/strona_glowna.html'

class KryteriaOceny(TemplateView):
    template_name = 'website/kryteria_oceny.html'

class Kontakt(TemplateView):
    template_name = 'website/kontakt.html'

class Logowanie(TemplateView):
    template_name = 'website/logowanie.html'

def EdytujStudenta(request,pk):
    student = Student.objects.get(id_student=pk)
    form = StudentRegistrationForm(instance=student)
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/admin_tables')
    context = {'form': form}
    return render(request, 'website/edytuj_studenta.html',context)

def UsunStudenta(request,pk):
    student = Student.objects.get(id_student=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('/admin_tables')
    context = {'item': student}
    return render(request, 'website/usun_studenta.html',context)


def EdytujFormNiepelno(request,pk):
    formularz = Formularz.objects.get(id_formularza=pk)
    form = SkladanieFormularzaDlaNiepelnosprawnych(instance=formularz)
    if request.method == 'POST':
        form = SkladanieFormularzaDlaNiepelnosprawnych(request.POST, instance=formularz)
        if form.is_valid():
            form.save()
            return redirect('/admin_tables')
    context = {'form': form}
    return render(request, 'website/edytuj_form_niepelno.html',context)

def UsunFormNiepelno(request,pk):
    formularz = Formularz.objects.get(id_formularza=pk)
    if request.method == 'POST':
        formularz.delete()
        return redirect('/admin_tables')
    context = {'item': formularz}
    return render(request, 'website/usun_form_niepelno.html',context)
