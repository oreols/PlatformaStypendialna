from django.urls import path
from .views import *
from .views import Formularze, Kontakt, Logowanie

urlpatterns = [
    path('', main),
    path('login', loginPage),
    path('register', registerPage, name='register'),
    path('formularze', Formularze.as_view(), name='formularze'),
    path('kontakt', Kontakt.as_view(), name='kontakt'),
    path('logowanie', Logowanie.as_view(), name='logowanie'),
    path('form_niepelno', ZlozenieFormularzaNiepelnosprawnych, name='skladanieformularzudlaniepelnosprawnych')
]