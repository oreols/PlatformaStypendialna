from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.http import HttpResponse;
from django.forms import formset_factory
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
from .models import Student, Formularz, Kontakt, Aktualnosci, CzlonekRodziny
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.urls import reverse

from .forms import StudentRegistrationForm, SkladanieFormularzaDlaNiepelnosprawnych, ZapiszOsiagniecie, KontaktForm, AktualnosciForm, FormularzSocjalne, CzlonekSocjalne
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

def ZlozenieFormularzaNaukowego(request):
    OsiagnieciaFormSet = formset_factory(ZapiszOsiagniecie, extra=13)
    formset = OsiagnieciaFormSet()

    texts = [
        "Autorstwo lub współautorstwo publikacji naukowych w czasopismach naukowych ujętych w wykazie ogłoszonym przez ministra właściwego do spraw nauki, PKT 0,03",
        "Autorstwo lub współautorstwo rozdziału książki, PKT 0,02",
        "Autorstwo lub współautorstwo artykułu w publikacji pokonferencyjnej, PKT 0,01",
        "Referaty własne wygłoszone samodzielnie na konferencjach naukowych, w których uczestniczyli prelegenci ośrodków akademickich, PKT 0,01",
        "Nagrody uzyskane w konkursach o zasięgu międzynarodowym, PKT 0,01",
        "Nagrody uzyskane w konkursach o zasięgu krajowym, w których uczestniczyli studenci ośrodków akademickich, PKT 0,01",
        "Czynny udział w pracach koła naukowego, PKT 0,01",
        "Autorstwo, współautorstwo dzieł artystycznych, w tym plastycznych, muzycznych, teatralnych lub filmowych, wydanych w nakładzie co najmniej 500 egzemplarzy, PKT 0,05",
        "Wykonanie dzieł artystycznych, w tym plastycznych, muzycznych, teatralnych lub filmowych, zaprezentowanych publicznie na festiwalach, wystawach lub przeglądach, o znaczeniu co najmniej krajowym, PKT 0,03",
        "Nagrody uzyskane w konkursach artystycznych o znaczeniu międzynarodowym, PKT 0,03",
        "Nagrody uzyskane w konkursach plastycznych o zasięgu krajowym, w których uczestniczyli studenci z innych ośrodków akademickich, PKT 0,02",
        "Uzyskanie, co najmniej dziesiątego miejsca w igrzyskach olimpijskich, ósmego miejsca w mistrzostwach świata, piątego miejsca w młodzieżowych mistrzostwach świata lub mistrzostwach Europy, trzeciego miejsca w młodzieżowych mistrzostwach Europy, PKT 0,05",
        "Uzyskanie, co najmniej trzeciego miejsca w akademickich mistrzostwach Polski, PKT 0,02"
    ]
    
    if request.method == 'POST':
        formset = OsiagnieciaFormSet(request.POST)
        for form in formset:
            if form.has_changed():
                form.save()
    else:
        form = ZapiszOsiagniecie()
    
    form_text_list  = zip(formset, texts)
    
    return render (request, 'website/form_naukowe.html', {'formset': formset, 'form_text_list': form_text_list})


def AdminTables(request):
    student = Student.objects.all()
    formularz = Formularz.objects.all()
    kontakt = Kontakt.objects.all()
    aktualnosci = Aktualnosci.objects.all()
    context = {'student': student , 'formularz': formularz, 'kontakt': kontakt, 'aktualnosci': aktualnosci}
    return render(request, 'website/admin_tables.html', context)

class PanelAdmina(TemplateView):
    template_name = 'website/panel_admina.html'
class Formularze(TemplateView):
    template_name = 'website/formularze.html'

class StronaGlowna(TemplateView):
    template_name = 'website/strona_glowna.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pobierz ostatnią aktualność
        ostatnia_aktualnosc = Aktualnosci.objects.last()
        context['ostatnia_aktualnosc'] = ostatnia_aktualnosc
        return context

class KryteriaOceny(TemplateView):
    template_name = 'website/kryteria_oceny.html'

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

class Kontakty(TemplateView):
    template_name = 'website/kontakt.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ostatni_kontakt = Kontakt.objects.last()
        context['ostatni_kontakt'] = ostatni_kontakt
        if self.request.user.is_superuser:
            context['form'] = KontaktForm(instance=ostatni_kontakt)
        return context

def edytujKontakt(request):
    kontakt = Kontakt.objects.last()
    if request.method == 'POST':
        form = KontaktForm(request.POST, instance=kontakt)
        if form.is_valid():
            form.save()
            return redirect('kontakt')
    else:
        form = KontaktForm(instance=kontakt)
    return render(request, 'website/edytuj_kontakt.html', {'form': form})


def dodajAktualnosc(request):
    if request.method == 'POST':
        aktualnosci = AktualnosciForm(request.POST)
        if aktualnosci.is_valid():
            aktualnosci.save()
            return redirect('strona_glowna')
    else:
        aktualnosci = AktualnosciForm()
    return render(request, 'website/dodaj_aktualnosci.html', {'form': aktualnosci})

def edytujAktualnosc(request,pk):
    aktualnosci = Aktualnosci.objects.get(id_aktualnosci=pk)
    form = AktualnosciForm(instance=aktualnosci)
    if request.method == 'POST':
        form = AktualnosciForm(request.POST, instance=aktualnosci)
        if form.is_valid():
            form.save()
            return redirect('/admin_tables')
    context = {'form': form}
    return render(request, 'website/edytuj_aktualnosci.html',context)


def ZlozenieFormularzaSocjalnego(request):
    if request.method == 'POST':
        form_soc = FormularzSocjalne(request.POST)
        print("Formularz otrzymany:", form_soc)
        if form_soc.is_valid():
            student = request.user
            form_soc_instance = form_soc.save(commit=False)  # Zapisuje formularz ale jeszcze nie w bazie
            czlonek = CzlonekSocjalne(request.POST)
            if czlonek.is_valid():
                czlonek_instance = czlonek.save(commit=False)  # Zapisuje czlonka ale tez nie w bazie jeszcze
                form_soc_instance.student = student
                czlonek_instance.student = student
                form_soc_instance.save()  # Teraz zapisuje formularz w bazie
                czlonek_instance.save()  # Teraz zapisuje członka w bazie
                return redirect('/admin_tables')
    else:
        form_soc = FormularzSocjalne()
        czlonek = CzlonekSocjalne()
    return render(request, 'website/form_socjalne.html', {'form_soc': form_soc, 'czlonek': czlonek})


def EdytujFormSocjalne(request, pk_form, pk_czlonek):
    formularz = Formularz.objects.get(id_formularza=pk_form)
    czlonek = CzlonekRodziny.objects.get(id_czlonka=pk_czlonek)
    form_soc = FormularzSocjalne(instance=formularz)
    czlonek_form = CzlonekSocjalne(instance=czlonek)
    if request.method == 'POST':
        form_soc = FormularzSocjalne(request.POST, instance=formularz)
        czlonek_form = CzlonekSocjalne(request.POST, instance=czlonek)
        if form_soc.is_valid() and czlonek_form.is_valid():
            form_soc.save()
            czlonek_form.save()
            return redirect('/admin_tables')
    context = {'form_soc': form_soc, 'czlonek': czlonek_form}
    return render(request, 'website/edytuj_form_socjalne.html',context)

def UsunFormSocjalne(request,pk_form, pk_czlonek):
    formularz = Formularz.objects.get(id_formularza=pk_form)
    czlonek = CzlonekRodziny.objects.get(id_czlonka=pk_czlonek)
    if request.method == 'POST':
        formularz.delete()
        czlonek.delete()
        return redirect('/admin_tables')
    context = {'item': formularz}
    return render(request, 'website/usun_form_socjalne.html',context)