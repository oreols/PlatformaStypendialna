from django.urls import path
from .views import *
from .views import Formularze, Kontakt, Logowanie

urlpatterns = [
    path('', main, name = 'main'),
    path('rejestracja', registerPage, name='register'),
    path('formularze', Formularze.as_view(), name='formularze'),
    path('strona_glowna', StronaGlowna.as_view(), name='strona_glowna'),
    path('kryteria_oceny', KryteriaOceny.as_view(), name='kryteria_oceny'),
    path('kontakt', Kontakt.as_view(), name='kontakt'),
    path('logowanie', loginPage, name='logowanie'),
    path('form_niepelno', ZlozenieFormularzaNiepelnosprawnych, name='form_niepelno'),
    path('admin_tables', PanelAdmina, name='admin_tables'),
    path('edytuj_studenta/<str:pk>/', EdytujStudenta, name='edytuj_studenta'),
    path('usun_studenta/<str:pk>/', UsunStudenta, name='usun_studenta'),
    path('edytuj_form_niepelno/<str:pk>/', EdytujFormNiepelno, name='edytuj_form_niepelno'),
    path('usun_form_niepelno/<str:pk>/', UsunFormNiepelno, name='usun_form_niepelno'),
]