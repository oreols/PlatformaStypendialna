from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.http import HttpResponse;
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.encoding import force_bytes, force_str 
from .authbackend import CustomAuthBackend
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .models import Student, Formularz
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.urls import reverse

from .forms import StudentRegistrationForm, SkladanieFormularzaDlaNiepelnosprawnych
# Create your views here.

def main(request):
    return HttpResponse("Witam na platformie stypendialnej!")

def logoutUser(request):
    logout(request)
    return redirect('index')


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

def index(request):
    messages_to_display = messages.get_messages(request)
    return render(request, 'index.html', {'messages': messages_to_display})

def registerPage(request):
    form = StudentRegistrationForm()
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            #id_student = request.POST['id_student']
            form.instance.password = make_password(password)
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            User = get_user_model()
            user_object = User.objects.get(username=username)
            

            

            current_site = get_current_site(request)
            mail_subject = 'Aktywuj swoje konto'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user_object.pk)),
                'token': account_activation_token.make_token(user_object),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Proszę sprawdź swoją skrzynkę pocztową, aby aktywować konto')
            return redirect('index')
            #return render(request, 'website/logowanie.html', {'form': form})
    else:
        form = StudentRegistrationForm()
    return render(request, 'website/rejestracja.html', {'form': form})
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        user = None
    #user = User._default_manager.get(username=uid)
    if user is not None:
        messages.success(request, str(user))
    else:
        messages.error(request, str(user))
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user)

        messages.success(request, 'Konto zostało aktywowane')
        return redirect(reverse('logowanie'))
    else:
        messages.error(request, 'Link aktywacyjny jest nieprawidłowy lub przedawniony')
        return redirect('index')
        
        
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

#def ZlozenieFormularzaNaukowego(request, pk):
    #if request.method == 'POST':


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