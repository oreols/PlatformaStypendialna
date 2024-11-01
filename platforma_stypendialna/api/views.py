import logging

logger = logging.getLogger(__name__)
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
from .models import Student, Formularz, Kontakt, Aktualnosci, CzlonekRodziny, Osiagniecia
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.urls import reverse
from django.db import connection
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.utils import timezone
my_date = timezone.now()

from .forms import StudentRegistrationForm, SkladanieFormularzaDlaNiepelnosprawnych, ZapiszOsiagniecie, KontaktForm, AktualnosciForm, FormularzSocjalne, CzlonekSocjalne, SkladanieFormularzaNaukowego, ZapiszOsiagniecie, SemestrStudentaForm, AktualnySemestrForm, UpdateUzytkownik, CzlonekSocjalneFormSet
from django.core.exceptions import ValidationError
from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.http import Http404
from django.db import transaction
from django.urls import reverse
from django.db import connection
from django.forms.models import inlineformset_factory


# Create your views here.

def student_has_submitted_form_naukowe(student_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM api_formularz WHERE student_id = %s AND typ_stypendium = 'naukowe' AND status != 'archiwalne' ", [student_id])
        row = cursor.fetchone()
    return row[0] > 0

def student_has_submitted_form_socjalne(student_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM api_formularz WHERE student_id = %s AND typ_stypendium = 'socjalne' AND status != 'archiwalne' ", [student_id])
        row = cursor.fetchone()
    return row[0] > 0

def student_has_submitted_form_niepelnosprawne(student_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM api_formularz WHERE student_id = %s AND typ_stypendium = 'dla_niepelnosprawnych' AND status != 'archiwalne' ", [student_id])
        row = cursor.fetchone()
    return row[0] > 0

#def zapisz_plec(student_id, pesel):
 #   query = """
  #  UPDATE api_student SET plec = ustal_plec(pesel) WHERE student_id = %s AND plec IS NULL", [pesel, student_id])
   # """
    #return Student.objects.raw(query)    

#def zapisz_plec(pesel, numer_albumu):
 #   with connection.cursor() as cursor:
  #      cursor.execute("UPDATE api_student SET plec = ustal_plec(%s) WHERE numer_albumu = %s", [pesel, numer_albumu])

def zapisz_plec(pesel):
    if len(pesel) != 11 or not pesel.isdigit():
        raise ValueError("Zle podany pesel")

    literka_plec = int(pesel[9])
    return 'F' if literka_plec % 2 == 0 else 'M'

def ranking_studentow():
    query = """
        SELECT api_student.numer_albumu, api_student.id_student, api_formularz.srednia_ocen
        FROM api_student INNER JOIN api_formularz ON api_formularz.student_id = api_student.id_student
        WHERE api_formularz.typ_stypendium = 'naukowe' AND api_formularz.status = 'zaakceptowane'
        ORDER BY api_formularz.srednia_ocen DESC
    """
    return Student.objects.raw(query)
    

@login_required
def widok_ranking_studentow(request):
    students = ranking_studentow()
    return render(request, 'website/ranking.html', {'students': students})

def main(request):
    return HttpResponse("Witam na platformie stypendialnej!")

def logoutUser(request):
    logout(request)
    return redirect('logowanie')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('profil_uzytkownika')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('strona_glowna')
        else:
            return HttpResponse("Nieprawidłowa nazwa użytkownika lub hasło")
        
    return render(request, 'website/logowanie.html')

def index(request):
    messages_to_display = messages.get_messages(request)
    return render(request, 'index.html', {'messages': messages_to_display})

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('profil_uzytkownika')
    form = StudentRegistrationForm()
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            #id_student = request.POST['id_student']
            form.instance.password = make_password(password)
            form.instance.plec = zapisz_plec(form.instance.pesel)
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

@login_required   
def ZlozenieFormularzaNiepelnosprawnych(request):
    if request.method == 'POST':
        form = SkladanieFormularzaDlaNiepelnosprawnych(request.POST)
        student = request.user
        form.instance.student = student
        form.save(commit=False)
        if not student_has_submitted_form_socjalne(form.instance.student.id_student):
            if not student_has_submitted_form_niepelnosprawne(form.instance.student.id_student):
                #student = request.user
                if form.is_valid():
                    #form.instance.student = student
                    form.save()
                    return redirect('strona_glowna')
            else:
                messages_to_display = 'Skladales juz formularz dla niepelnosprawnych'
                return render(request, 'website/index2.html', {'messages': messages_to_display})
        else:
            messages_to_display = 'Skladales juz formularz socjalny'
            return render(request, 'website/index2.html', {'messages': messages_to_display})
    else:
        form = SkladanieFormularzaDlaNiepelnosprawnych()
    return render(request, 'website/form_niepelno.html', {'form': form}) 

@login_required
def ZlozenieFormularzaNaukowego(request):
    OsiagnieciaFormSet = formset_factory(ZapiszOsiagniecie, extra=13)
    formset = OsiagnieciaFormSet()
    form_naukowe = SkladanieFormularzaNaukowego()
    form_student = Student.objects.get(username=request.user)

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
        srednia = float(request.POST["srednia_ocen"])
        
        form_naukowe = SkladanieFormularzaNaukowego(request.POST)
        if formset.is_valid() and form_naukowe.is_valid():
            student = request.user
            form_naukowe.instance.student = student
            form_naukowe.save(commit=False)
            #srednia = form_naukowe.srednia_ocen()
            if srednia >= form_student.nazwa_kierunku.srednia_kierunku and not student_has_submitted_form_naukowe(form_naukowe.instance.student.id_student):
                form_naukowe.save(commit=True)
                for form in formset:
                    if form.has_changed():
                        form.instance.student = student
                        form.save()
            else:
                messages_to_display = 'Niestety nie spełniasz wymaganej średniej lub składałeś już formularz naukowy'
                return render(request, 'website/index2.html', {'messages': messages_to_display})

        return redirect('/admin_tables')
    else:
        form = ZapiszOsiagniecie()
        form_naukowe = SkladanieFormularzaNaukowego()
    
    form_text_list  = zip(formset, texts)
    
    return render (request, 'website/form_naukowe.html', {'formset': formset, 'form_text_list': form_text_list, 'form_naukowe': form_naukowe, 'form_student': form_student})

@user_passes_test(lambda u: u.is_superuser)
def AdminTables(request):
    with connection.cursor() as cursor:
        cursor.callproc('CountStudents')
        results = cursor.fetchall()
        student_count = None
        for result in results:
            student_count = result[0] if result else None

    student = Student.objects.all()
    formularz = Formularz.objects.all()
    context = {'student': student , 'formularz': formularz,'student_count': student_count}
    return render(request, 'website/admin_tables.html', context)

@user_passes_test(lambda u: u.is_superuser)
def Konta(request):
    with connection.cursor() as cursor:
        cursor.callproc('CountStudents')
        results = cursor.fetchall()
        student_count = None
        for result in results:
            student_count = result[0] if result else None

    student = Student.objects.all()
    context = {'student': student, 'student_count': student_count}
    return render(request, 'website/konta.html', context)

@user_passes_test(lambda u: u.is_superuser)
def Statystyki(request):
    with connection.cursor() as cursor:
        cursor.callproc('UsunPusteFormularze')
    with connection.cursor() as cursor:
        cursor.callproc('CountWnioski')
        result = cursor.fetchone()
        wnioski_count = result[0] if result else 0

    with connection.cursor() as cursor:
        cursor.callproc('CountSocjalne')
        result = cursor.fetchone()
        count_socjalne = result[0] if result else 0
        count_socjalne_zaakceptowane = result[1] if result else 0
        count_socjalne_odrzucone = result[2] if result else 0

    with connection.cursor() as cursor:
        cursor.callproc('CountNaukowe')
        result = cursor.fetchone()
        count_naukowe = result[0] if result else 0
        count_naukowe_zaakceptowane = result[1] if result else 0
        count_naukowe_odrzucone = result[2] if result else 0

    with connection.cursor() as cursor:
        cursor.callproc('CountNiepelno')
        result = cursor.fetchone()
        count_niepelno = result[0] if result else 0
        count_niepelno_zaakceptowane = result[1] if result else 0
        count_niepelno_odrzucone = result[2] if result else 0

    with connection.cursor() as cursor:
        cursor.callproc('CountStudents')
        result = cursor.fetchone()
        student_count = result[0] if result else 0

    context = {
        'count_socjalne': count_socjalne,
        'count_naukowe': count_naukowe,
        'count_niepelno': count_niepelno,
        'student_count': student_count,
        'wnioski_count': wnioski_count,
        'count_niepelno_zaakceptowane': count_niepelno_zaakceptowane,
        'count_socjalne_zaakceptowane': count_socjalne_zaakceptowane,
        'count_naukowe_zaakceptowane': count_naukowe_zaakceptowane,
        'count_niepelno_odrzucone': count_niepelno_odrzucone,
        'count_socjalne_odrzucone': count_socjalne_odrzucone,
        'count_naukowe_odrzucone': count_naukowe_odrzucone,
    }
    return render(request, 'website/statystyki.html', context)

@user_passes_test(lambda u: u.is_superuser)
def NoweWnioski(request):
    formularz = Formularz.objects.all()
    context = {'formularz': formularz}
    return render(request, 'website/nowe_wnioski.html', context)

@user_passes_test(lambda u: u.is_superuser)
def PanelAdmina(request):
    return render(request, 'website/panel_admina.html')

@login_required
def Formularze(request):
    return render(request, 'website/formularze.html')

@user_passes_test(lambda u: u.is_superuser)
def PanelRektora(request):
    return render(request, 'website/panel_rektora.html')


def StronaGlowna(request):
    return render(request, 'website/strona_glowna.html')


class Wyniki(TemplateView):
    template_name = 'website/wyniki.html'


class StronaGlowna(TemplateView):
    template_name = 'website/strona_glowna.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT nazwa_aktualnosci, tekst_aktualnosci, data_opublikowania
                    FROM api_aktualnosci
                    ORDER BY data_opublikowania DESC
                    LIMIT 1
                """)
                row = cursor.fetchone()
                if row:
                    ostatnia_aktualnosc = {
                        'nazwa_aktualnosci': row[0],
                        'tekst_aktualnosci': row[1],
                        'data_opublikowania': row[2]
                    }
                else:
                    ostatnia_aktualnosc = None

        context['ostatnia_aktualnosc'] = ostatnia_aktualnosc
        return context

def KryteriaOceny(request):
    return render(request, 'website/kryteria_oceny.html')

def Logowanie(request):
    return render(request, 'website/logowanie.html')

@user_passes_test(lambda u: u.is_superuser)
def EdytujStudenta(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT username, pesel, numer_albumu
            FROM api_student 
            WHERE id_student = %s
        """, [pk])
        student = cursor.fetchone()
    
    if request.method == 'POST':
        username = request.POST.get('username')
        pesel = request.POST.get('pesel')
        numer_albumu = request.POST.get('numer_albumu')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE api_student
                SET username = %s, pesel = %s, numer_albumu = %s
                WHERE id_student = %s
            """, [username, pesel, numer_albumu, pk])

        return redirect('/admin_tables')

    context = {
        'student': {
            'username': student[0],
            'pesel': student[1],
            'numer_albumu': student[2]
        }
    }
    return render(request, 'website/edytuj_studenta.html', context)

@user_passes_test(lambda u: u.is_superuser)
def UsunStudenta(request,pk):
    student = Student.objects.get(id_student=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('/konta')
    context = {'item': student}
    return render(request, 'website/usun_studenta.html',context)

@user_passes_test(lambda u: u.is_superuser)
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

@user_passes_test(lambda u: u.is_superuser)
def ZobaczFormNiepelno(request, pk):
    formularz = get_object_or_404(Formularz, id_formularza=pk)
    
    if request.method == 'POST':
        form = SkladanieFormularzaDlaNiepelnosprawnych(request.POST, instance=formularz)
        if form.is_valid():
            if 'accept' in request.POST:
                formularz.status = 'zaakceptowane'
                formularz.save()
                return redirect('zaakceptowane_wnioski')
            elif 'reject' in request.POST:
                formularz.status = 'odrzucone'
                formularz.save()
                return redirect('odrzucone_wnioski')
    else:
        form = SkladanieFormularzaDlaNiepelnosprawnych(instance=formularz)

    context = {'form': form}
    return render(request, 'website/zobacz_form_niepelno.html', context)

@user_passes_test(lambda u: u.is_superuser)
def ZobaczFormSocjalne(request, pk):
    formularz = get_object_or_404(Formularz, id_formularza=pk)
    
    if request.method == 'POST':
        form = FormularzSocjalne(request.POST, instance=formularz)
        if 'accept' in request.POST:
            formularz.status = 'zaakceptowane'
            formularz.save()
            return redirect('zaakceptowane_wnioski')
        elif 'reject' in request.POST:
            if form.is_valid():
                formularz.status = 'odrzucone'
                formularz.save()
                return redirect('odrzucone_wnioski')
    else:
        form = FormularzSocjalne(instance=formularz)
    
    context = {'form': form}
    return render(request, 'website/zobacz_form_socjalne.html', context)

@user_passes_test(lambda u: u.is_superuser)
def ZobaczFormNaukowe(request, pk):
    formularz = get_object_or_404(Formularz, id_formularza=pk)

    if request.method == 'POST':
        form = SkladanieFormularzaNaukowego(request.POST, instance=formularz)
        if 'accept' in request.POST:
            formularz.status = 'zaakceptowane'
            formularz.save()
            return redirect('zaakceptowane_wnioski')
        elif 'reject' in request.POST:
            if form.is_valid():
                formularz.status = 'odrzucone'
                formularz.save()
                return redirect('odrzucone_wnioski')
    else:
        form = SkladanieFormularzaNaukowego(instance=formularz)
    
    context = {'form_n': form}
    return render(request, 'website/zobacz_form_naukowe.html', context)

@user_passes_test(lambda u: u.is_superuser)
def AkceptowaneWnioski(request):
    query = "SELECT * FROM api_formularz WHERE status = %s"
    params = ['zaakceptowane']
    formularze = Formularz.objects.raw(query, params)
    return render(request, 'website/zaakceptowane_wnioski.html', {'formularze': formularze})

@user_passes_test(lambda u: u.is_superuser)
def OdrzuconeWnioski(request):
    query = "SELECT * FROM api_formularz WHERE status = %s"
    params = ['odrzucone']
    formularze = Formularz.objects.raw(query, params)
    return render(request, 'website/odrzucone_wnioski.html', {'formularze': formularze})

@user_passes_test(lambda u: u.is_superuser)
def WszystkieWnioski(request):
    query = "SELECT * FROM api_formularz WHERE status NOT LIKE 'archiwalne'"
    formularze = Formularz.objects.raw(query)
    return render(request, 'website/wszystkie_wnioski.html', {'formularze': formularze})

@user_passes_test(lambda u: u.is_superuser)
def ArchiwalneWnioski(request):
    query = "SELECT * FROM api_formularz WHERE status = %s"
    params = ['archiwalne']
    formularze = Formularz.objects.raw(query, params)
    return render(request, 'website/archiwalne_wnioski.html', {'formularze': formularze})

@user_passes_test(lambda u: u.is_superuser)
def ArchiwizujWszystkieWnioski(request):
    nowy_status = 'archiwalne'
    
    update_query = "UPDATE api_formularz SET status = %s WHERE status != %s"
    with connection.cursor() as cursor:
        cursor.execute(update_query, [nowy_status, nowy_status])

    select_query = "SELECT * FROM api_formularz WHERE status = %s"
    formularze = Formularz.objects.raw(select_query, [nowy_status])
    
    return render(request, 'website/archiwalne_wnioski.html', {'formularze': formularze})


class Kontakty(TemplateView):
    template_name = 'website/kontakt.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT email,numer_tel
                FROM api_kontakt
                ORDER BY id_kontakt DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            if row:
                kontakt = {
                    'email': row[0],
                    'numer_tel': row[1]
                }
            else:
                kontakt = None
        context['kontakt'] = kontakt
        return context

@user_passes_test(lambda u: u.is_superuser)
def edytujKontakt(request):
    kontakt = Kontakt.objects.last()
    
    kontakt_lista = Kontakt.objects.all()
    if request.method == 'POST':
        form = KontaktForm(request.POST, instance=kontakt)
        if form.is_valid():
            form.save()
            return redirect('edytuj_kontakt')
    else:
        form = KontaktForm(instance=kontakt)
    return render(request, 'website/edytuj_kontakt.html', {'form': form, 'kontakt_lista': kontakt_lista})

@user_passes_test(lambda u: u.is_superuser)
def dodajAktualnosc(request):
    aktualnosci_list = Aktualnosci.objects.all()
    if request.method == 'POST':
        aktualnosci = AktualnosciForm(request.POST)
        if aktualnosci.is_valid():
            aktualnosci.save()
            return redirect('dodaj_aktualnosci')
    else:
        aktualnosci = AktualnosciForm()
    return render(request, 'website/dodaj_aktualnosci.html', {'form': aktualnosci, 'aktualnosci_list': aktualnosci_list})

@user_passes_test(lambda u: u.is_superuser)
def edytujAktualnosc(request,pk):
    aktualnosci = Aktualnosci.objects.get(id_aktualnosci=pk)
    form = AktualnosciForm(instance=aktualnosci)
    if request.method == 'POST':
        form = AktualnosciForm(request.POST, instance=aktualnosci)
        if form.is_valid():
            form.save()
            return redirect('/dodaj_aktualnosci')
    context = {'form': form}
    return render(request, 'website/edytuj_aktualnosci.html',context)

@login_required
def ZlozenieFormularzaSocjalnego(request, id=None):
    if id:
        obj = get_object_or_404(Formularz, id=id)
    else:
        obj = None

    semestr_studenta = SemestrStudentaForm(request.POST or None, instance=obj)
    aktualny_semestr = AktualnySemestrForm(request.POST or None, instance=obj)
    form_soc = FormularzSocjalne(request.POST or None, instance=obj)
    CzlonekFormset = modelformset_factory(CzlonekRodziny, form=CzlonekSocjalne, extra=1, can_delete=True)
    
    if obj:
        formset = CzlonekFormset(request.POST or None, queryset=obj.czlonekrodziny_set.all())
    else:
        formset = CzlonekFormset(request.POST or None, queryset=CzlonekRodziny.objects.none())

    if request.method == 'POST':
        if form_soc.is_valid() and formset.is_valid() and semestr_studenta.is_valid() and aktualny_semestr.is_valid():
           
            if not form_soc.has_changed() and not any(form.has_changed() for form in formset):
                messages.error(request, "Nie wypełniono żadnych pól formularza.")
            else:
                student = request.user
                
               
                with transaction.atomic():
                    semestr_studenta_instance = semestr_studenta.save(commit=False)
                    semestr_studenta_instance.student = student
                    semestr_studenta_instance.save()
                    
                    aktualny_semestr_instance = aktualny_semestr.save(commit=False)
                    aktualny_semestr_instance.student = student
                    aktualny_semestr_instance.save()
                    
                    form_soc_instance = form_soc.save(commit=False)
                    form_soc_instance.student = student
                    form_soc_instance.save()

                    for form in formset:
                        if form.cleaned_data.get('DELETE'):
                            if form.instance.pk:
                                form.instance.delete()
                        else:
                            czlonek_instance = form.save(commit=False)
                            czlonek_instance.student = student
                            czlonek_instance.save()

                return redirect('/admin_tables')
        
    context = {
        'form_soc': form_soc,
        'formset': formset,
        'semestr_studenta': semestr_studenta,
        'aktualny_semestr': aktualny_semestr
    }
    return render(request, 'website/form_socjalne.html', context)


@user_passes_test(lambda u: u.is_superuser)
def EdytujFormSocjalne(request, pk_form, pk_student):
    formularz = get_object_or_404(Formularz, id_formularza=pk_form)
    czlonek_rows = CzlonekRodziny.objects.filter(student_id=pk_student)
    
    if request.method == 'POST':
        form_soc = FormularzSocjalne(request.POST, instance=formularz)
        czlonek_formset = CzlonekSocjalneFormSet(request.POST, queryset=czlonek_rows)
        
        if form_soc.is_valid() and czlonek_formset.is_valid():
            form_soc.save()
            czlonek_formset.save()
            return redirect('/admin_tables')
    else:
        form_soc = FormularzSocjalne(instance=formularz)
        czlonek_formset = CzlonekSocjalneFormSet(queryset=czlonek_rows)
    
    context = {'form_soc': form_soc, 'czlonek_formset': czlonek_formset}
    return render(request, 'website/edytuj_form_socjalne.html', context)

@user_passes_test(lambda u: u.is_superuser)
def UsunFormNiepelno(request, pk):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM api_historiastatusow WHERE formularz_id = %s", [pk])
            cursor.execute("DELETE FROM api_formularz WHERE id_formularza = %s", [pk])
        return render(request, 'website/usun_form_niepelno.html')
    return render(request, 'website/usun_form_niepelno.html')




@user_passes_test(lambda u: u.is_superuser)
def UsunFormSocjalne(request, pk_form, pk_student):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM api_historiastatusow WHERE formularz_id = %s", [pk_form])
            cursor.execute("DELETE FROM api_czlonekrodziny WHERE student_id = %s", [pk_student])
            cursor.execute("DELETE FROM api_formularz WHERE id_formularza = %s", [pk_form])
        
        return redirect(reverse('admin_tables'))
    return render(request, 'website/usun_form_socjalne.html')

@user_passes_test(lambda u: u.is_superuser)
def EdytujFormNaukowe(request, pk_form):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_formularza, typ_stypendium, data_zlozenia, srednia_ocen, aktualny_semestr_id, semestr_studenta_id FROM api_formularz WHERE id_formularza = %s", [pk_form])
        

    formularz = Formularz.objects.get(id_formularza=pk_form)
    form_naukowe = SkladanieFormularzaNaukowego(instance=formularz)
    if request.method == 'POST':
        form_naukowe = SkladanieFormularzaNaukowego(request.POST, instance=formularz)
        if form_naukowe.is_valid():
            form_naukowe.save()
            return redirect('/admin_tables')
    context = {'form_naukowe': form_naukowe}
    return render(request, 'website/edytuj_form_naukowe.html',context)

@user_passes_test(lambda u: u.is_superuser)
def UsunFormNaukowe(request,pk_form):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM api_historiastatusow WHERE formularz_id = %s", [pk_form])
            cursor.execute("DELETE FROM api_formularz WHERE id_formularza = %s", [pk_form])
        return redirect('/admin_tables')
    return render(request, 'website/usun_form_naukowe.html')

@login_required
def AktualizujProfil(request):
    if request.method == 'POST':
        form = UpdateUzytkownik(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profil_uzytkownika')
    else:
        form = UpdateUzytkownik(instance=request.user)
    context = {'form': form}

    return render(request, 'website/profil_uzytkownika.html', context)

@login_required
def WynikiStudenta(request):
    user = request.user
    student_id = user.id_student

    query = """
        SELECT f.typ_stypendium, f.status, f.data_zlozenia, h.data_zmiany, h.data_zlozenia_form
        FROM api_formularz f
        LEFT JOIN api_historiastatusow h ON f.id_formularza = h.formularz_id
        WHERE f.student_id = %s 
        ORDER BY f.id_formularza
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [student_id])
        rows = cursor.fetchall()

    forms = []
    current_form = None

    for row in rows:
        typ_stypendium, status, data_zlozenia, data_zmiany, data_zlozenia_form = row

        if current_form is None or current_form['typ_stypendium'] != typ_stypendium:
            if current_form is not None:
                forms.append(current_form)
            current_form = {
                'typ_stypendium': typ_stypendium,
                'status': status,
                'data_zlozenia': data_zlozenia,
                'historia': []
            }

        if data_zmiany:
            current_form['historia'].append({
                'data_zlozenia_form': data_zlozenia_form,
                'data_zmiany': data_zmiany,
            })

    if current_form is not None:
        forms.append(current_form)

    context = {'forms': forms}

    return render(request, 'website/wyniki.html', context)
