from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from .views import Formularze, Kontakt, Logowanie

urlpatterns = [
    #path('', main, name = 'main'),
    path('rejestracja', registerPage, name='register'),
    path('logout', logoutUser, name='logout'),
    path('index', index, name='index'),
    path('formularze', Formularze, name='formularze'),
    path('', StronaGlowna, name='strona_glowna'),
    #path('strona_glowna', StronaGlowna.as_view(), name='strona_glowna'),
    path('kryteria_oceny', KryteriaOceny, name='kryteria_oceny'),
    #path('account_activation_email', )
    path('kontakt', Kontakty.as_view(), name='kontakt'),
    path('password_reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm', auth_views.PasswordResetDoneView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetDoneView.as_view(), name='password_reset_complete'),
    path('password_change', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('logowanie', loginPage, name='logowanie'),
    path('form_niepelno', ZlozenieFormularzaNiepelnosprawnych, name='form_niepelno'),
    path('edytuj_studenta/<str:pk>/', EdytujStudenta, name='edytuj_studenta'),
    path('usun_studenta/<str:pk>/', UsunStudenta, name='usun_studenta'),
    path('edytuj_form_niepelno/<str:pk>/', EdytujFormNiepelno, name='edytuj_form_niepelno'),
    path('usun_form_niepelno/<str:pk>/', UsunFormNiepelno, name='usun_form_niepelno'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('form_naukowe', ZlozenieFormularzaNaukowego, name='form_naukowe'),
    path('panel_admina', PanelAdmina, name='panel_admina'),
    path('edytuj_kontakt', edytujKontakt, name='edytuj_kontakt'),
    path('admin_tables', AdminTables, name='admin_tables'),
    path('dodaj_aktualnosci', dodajAktualnosc, name='dodaj_aktualnosci'),
    path('edytuj_aktualnosci/<str:pk>/', edytujAktualnosc, name='edytuj_aktualnosci'),
    path('form_socjalne', ZlozenieFormularzaSocjalnego, name='form_socjalne'),
    path('edytuj_form_socjalne/<str:pk_form>/', EdytujFormSocjalne, name='edytuj_form_socjalne'),
    path('usun_form_socjalne/<str:pk_form>/', UsunFormSocjalne, name='usun_form_socjalne'),
    path('edytuj_form_naukowe/<str:pk_form>/', EdytujFormNaukowe, name='edytuj_form_naukowe'),
    path('usun_form_naukowe/<str:pk_form>/', UsunFormNaukowe, name='usun_form_naukowe'),
    path('panel_rektora', PanelRektora, name='panel_rektora'),
    path('nowe_wnioski', NoweWnioski, name='nowe_wnioski'),
    path('zobacz_form_niepelno/<int:pk>/', ZobaczFormNiepelno, name='zobacz_form_niepelno'),
    path('zobacz_form_socjalne/<int:pk>/', ZobaczFormSocjalne, name='zobacz_form_socjalne'),
    path('zobacz_form_naukowe/<int:pk>/', ZobaczFormNaukowe, name='zobacz_form_naukowe'),
    path('zaakceptowane_wnioski', AkceptowaneWnioski, name='zaakceptowane_wnioski'),
    path('odrzucone_wnioski/', OdrzuconeWnioski, name='odrzucone_wnioski'),
]