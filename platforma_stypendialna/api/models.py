from datetime import timezone
from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.core.exceptions import ValidationError

def validate_digits_only(value):
        if not value.isdigit():
            raise ValidationError('Wpisz tylko cyfry.') 
def validate_string(value):
        if not value.isalpha():
            raise ValidationError('Wpisz tylko litery.')

class Kierunek(models.Model):
    id_kierunku = models.IntegerField(primary_key=True)
    nazwa_kierunku = models.TextField(null=True)

    def __str__(self):
        return self.nazwa_kierunku

class DecyzjeStypendialne(models.Model):
    id_decyzji = models.IntegerField(primary_key=True)
    id_student = models.IntegerField(null=True)
    decyzja = models.SmallIntegerField(null=True)

    def __str__(self):
        return str(self.id_decyzji)


class Formularz(models.Model):
    id_formularza = models.AutoField(primary_key=True)
    typ_stypendium = models.CharField(null=True, blank=True, max_length=30)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    data_zlozenia = models.DateTimeField(null=True, blank=True)
    przychod_bez_podatku = models.FloatField(null=True, blank=True)
    srednia_przychod = models.FloatField(null=True, blank=True)
    srednia_ocen = models.FloatField(null=True, blank=True)
    dodatkowe_informacje = models.TextField(null=True, blank=True)
    plik_orzeczenie = models.ImageField(null=True, blank=True, upload_to='dokumenty/orzeczenia') 
    id_osiagniecia = models.IntegerField(null=True, blank=True)
    zalacznik = models.FileField(null=True, blank=True, upload_to='dokumenty/zalaczniki')
    stopien_niepelnosprawnosci = models.ForeignKey('StopienNiepelnosprawnosci', on_delete=models.CASCADE, null=True, blank=True)
    symbol_niepelnosprawnosci = models.ForeignKey('SymbolNiepelnosprawnosci', on_delete=models.CASCADE, null=True, blank=True)
    charakter_stopnia_niepelnosprawnosci = models.TextField(null=True, blank=True, max_length=100)
    data_rozpoczecia_orzeczenia = models.DateField(null=True, blank=True)
    data_konca_orzeczenia = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('nowe', 'Nowe'), ('zaakceptowane', 'Zaakceptowane'), ('odrzucone', 'Odrzucone')], default='nowe', blank=True, null=True)
    komentarz = models.TextField(null=True, blank=True)
    punkty_osiagniecie = models.IntegerField(null=True, blank=True)
    aktualny_semestr = models.ForeignKey('AktualnySemestr', on_delete=models.CASCADE, null=True, blank=True)
    semestr_studenta = models.ForeignKey('SemestrStudenta', on_delete=models.CASCADE, null=True, blank=True)
    zalacznik_niepelnosprawnosc = models.FileField(null=True, blank=True, upload_to='dokumenty/zalaczniki_niepelnosprawnosci')   

def validate_string(value):
    if not value.isalpha():
        raise ValidationError('Wpisz tylko litery.')
    
class Student(AbstractUser):
    id_student = models.AutoField(primary_key=True, blank=True)  
    #nazwa_uzytkownika = models.CharField(null=True, unique=True, max_length = 20)
    #haslo = models.CharField(max_length = 100, null=True)
    email = models.CharField(null=True, unique=True, max_length=191)
    data_rejestracji = models.DateField(null=True)
    ikonka = models.ImageField(null=True, max_length = 180, blank=True, default='default.jpg', upload_to='dokumenty/ikonki')
    pesel = models.CharField(null=True, unique = True, max_length=11, validators=[validate_digits_only]) 
    imie = models.CharField(null=True, max_length=20, validators=[validate_string])
    nazwisko = models.CharField(null=True, max_length=35, validators=[validate_string])
    zalaczniki = models.FileField(null=True, upload_to='dokumenty/zalaczniki', blank = True)
    numer_telefonu = models.CharField(null=True, unique = True, max_length=9, validators=[validate_digits_only])
    nazwa_kierunku = models.ForeignKey(Kierunek, on_delete=models.CASCADE, null=True, blank=True)
    semestr = models.CharField(null=True, max_length=1, validators=[validate_digits_only])
    dodatkowe_punkty = models.IntegerField(null=True, blank=True, default=0)
    numer_albumu = models.CharField(null=True, max_length=5, validators=[validate_digits_only])
    rok_studiow = models.CharField(null=True, max_length=1, validators=[validate_digits_only])
    #kierunek = models.CharField(null=True,blank=True,max_length=50)
    ##decyzjeStypendialne = models.ForeignKey(DecyzjeStypendialne, on_delete=models.CASCADE)
    ##formularz = models.ForeignKey(Formularz, blank=True, null = True, on_delete=models.CASCADE)
    numer_konta_bankowego = models.CharField(null=True, max_length=26, validators=[validate_digits_only])

    #USERNAME_FIELD = 'nazwa_uzytkownika'
    REQUIRED_FIELDS = ['email', 'id_student']

    def __str__(self):
        return self.username
    
    
    
    
#class StudentManager(BaseUserManager):
    #def create_student(self, id_student, nazwa_uzytkownika, haslo, email, data_rejestracji, ikonka, pesel, imie, nazwisko, numer_telefonu, nazwa_kierunku, semestr, numer_albumu, rok_studiow, kierunek, numer_konta_bankowego):
        #if any(value is None for value in [id_student, nazwa_uzytkownika, haslo, email, data_rejestracji, ikonka, pesel, imie, nazwisko, numer_telefonu, nazwa_kierunku, semestr, numer_albumu, rok_studiow, kierunek, numer_konta_bankowego]):
            #raise ValueError("Ktores z podanych pól jest puste!")
        #student = self.create(id_student=id_student, nazwa_uzytkownika=nazwa_uzytkownika, haslo=haslo, email=email, data_rejestracji=data_rejestracji, ikonka=ikonka, pesel=pesel, imie=imie, nazwisko=nazwisko, numer_telefonu=numer_telefonu, nazwa_kierunku=nazwa_kierunku, semestr=semestr, numer_albumu=numer_albumu, rok_studiow=rok_studiow, kierunek=kierunek, numer_konta_bankowego=numer_konta_bankowego)
        #return student

class Admin(models.Model):
    id_admin = models.IntegerField(primary_key=True)
    haslo = models.TextField(null=True)
    login = models.TextField(null=True)
    email = models.TextField(null=True)
    def __str__(self):
        return self.login

class Aktualnosci(models.Model):
    id_aktualnosci = models.AutoField(primary_key=True)
    nazwa_aktualnosci = models.TextField(null=True)
    tekst_aktualnosci = models.TextField(null=True)
    data_opublikowania = models.DateField(null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id_aktualnosci)

class Kontakt(models.Model):
    id_kontakt = models.IntegerField(primary_key=True)
    email = models.TextField(null=True)
    numer_tel = models.IntegerField(null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id_kontakt)

class Przedmiot(models.Model):
    id_przedmiot = models.IntegerField(primary_key=True)
    nazwa_przedmiotu = models.TextField(null=True)
    id_kierunku = models.IntegerField(null=True)
    semestr = models.IntegerField(null=True)
    kierunek = models.ForeignKey(Kierunek, on_delete=models.CASCADE)
    punkty_ects = models.IntegerField(null=True)
    def __str__(self):
        return self.nazwa_przedmiotu

class OcenaKoncowa(models.Model):
    id_ocena = models.IntegerField(primary_key=True)
    id_student = models.IntegerField(null=True)
    ocena_koncowa = models.FloatField(null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    id_przedmiotu = models.IntegerField(null=True)
    przedmiot = models.ForeignKey(Przedmiot, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.student.imie) + " " + str(self.student.nazwisko) + " " + str(self.ocena_koncowa) + " " + str(self.przedmiot.nazwa_przedmiotu)

class Kryteria(models.Model):
    rok_kryterium = models.IntegerField(primary_key=True)
    srednia_ocen = models.FloatField(null=True)
    przychod_bez_podatku = models.FloatField(null=True)
    id_kierunku = models.IntegerField(null=True)
    id_formularza = models.IntegerField(null=True)
    wzor_stypendium = models.TextField(null=True)
    formularz = models.ForeignKey(Formularz, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.rok_kryterium)


class Ustawienia(models.Model):
    id_student = models.IntegerField(primary_key=True)
    nowe_haslo = models.TextField(null=True, blank=True)
    nowy_numer_konta_bankowego = models.TextField(null=True, blank=True)
    nowy_email = models.TextField(null=True, blank=True)
    nowe_imie = models.TextField(null=True, blank=True)
    nowe_nazwisko = models.TextField(null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE) 
    def __str__(self):
        return str(self.id_student)

class Ranking(models.Model):
    numer_albumu = models.IntegerField(primary_key=True)
    punkty_rankingu = models.CharField(max_length=45, null=True)
    typ_stypendium = models.CharField(max_length=65, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numer_albumu)

    

class DaneDziekanat(models.Model):
    numer_albumu = models.IntegerField(primary_key=True)
    ##ocena_koncowa = models.FloatField(null=True)
    imie = models.TextField(null=True)
    nazwisko = models.TextField(null=True)
    pesel = models.TextField(null=True)
    srednia_ocen = models.FloatField(null=True)
    id_przedmiot = models.IntegerField(null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    id_kierunku = models.IntegerField(null=True)

    def __str__(self):
        return str(self.numer_albumu)

class Powiadomienia(models.Model):
    id_powiadomienia = models.IntegerField(primary_key=True)
    tresc_powiadomienia = models.TextField(null=True)
    naglowek_powiadomienia = models.TextField(null=True)
    autor_powiadomienia = models.TextField(null=True)
    ##student_id_powiadomienie = models.IntegerField(null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_powiadomienia)

class KryteriaStrona(models.Model):
    id_wersja = models.IntegerField(primary_key=True)
    rok = models.TextField(null=True)
    tekst = models.TextField(null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_wersja)

class InformacjeStypendialne(models.Model):
    id_wersja = models.IntegerField(primary_key=True)
    tekst = models.TextField(null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_wersja)

class StudentLog(models.Model):
    id_log = models.IntegerField(primary_key=True)
    adres_ip = models.CharField(max_length=45, null=True)
    nazwa_uzytkownika = models.TextField(null=True)
    data_logowania = models.DateTimeField(null=True)
    ##haslo = models.TextField(null=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_log)

class AdminLog(models.Model):
    id_log_admin = models.IntegerField(primary_key=True)
    adres_ip = models.TextField(null=True)
    login = models.TextField(null=True)
    data_logowania = models.DateTimeField(null=True)
    ##haslo = models.TextField(null=True)
    def __str__(self):
        return str(self.id_log_admin)

#class Typ_Osiagniecia(models.Model):
    #id_typ_osiagniecia = models.IntegerField(primary_key=True)
    #nazwa_typu = models.TextField(null=True)
    #punkty_osiagniecie = models.IntegerField(null=True)

    #def __str__(self):
        #return str(self.nazwa_konkursu)

class Osiagniecia(models.Model):
    id_osiagniecia = models.AutoField(primary_key=True)
    #id_student = models.IntegerField(null=True)
    liczba_osiagniec = models.IntegerField(null=True,blank=True)
    #typ_osiagniecia = models.ForeignKey('Typ_Osiagniecia', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True, blank=True)
    krotki_opis = models.TextField(null=True, max_length=250, blank=True)
    data_osiagniecia = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.id_osiagniecia)

class OcenaKoncowaDziekanat(models.Model):
    id_ocena = models.IntegerField(primary_key=True)
    numer_albumu = models.IntegerField(null=True)
    ocena_koncowa = models.FloatField(null=True)
    id_przedmiotu = models.IntegerField(null=True)
    dane_dziekanat = models.ForeignKey('DaneDziekanat', on_delete=models.CASCADE)
    przedmiot = models.ForeignKey('Przedmiot', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.dane_dziekanat.imie) + " " + str(self.dane_dziekanat.nazwisko) + " " + str(self.ocena_koncowa) + " " + str(self.przedmiot.nazwa_przedmiotu)
    
class CzlonekRodziny(models.Model):
    id_czlonka = models.AutoField(primary_key=True)
    imie_czlonka = models.TextField(null=True)
    nazwisko_czlonka = models.TextField(null=True)
    stopien_pokrewienstwa = models.TextField(max_length=10, null=True)
    id_czlonka = models.IntegerField(primary_key=True)
    imie_czlonka = models.TextField(null=True, validators=[validate_string])
    nazwisko_czlonka = models.TextField(null=True, validators=[validate_string])
    stopien_pokrewienstwa = models.TextField(max_length=10, null=True, validators=[validate_string])
    data_urodzenia = models.DateField(null=True)
    miejsce_pracy = models.TextField(null=True, max_length=20)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)


    def __str__(self):
        return str(self.id_czlonka)
    
class SymbolNiepelnosprawnosci(models.Model):
    
    id_symbolu = models.IntegerField(primary_key=True)
    nazwa_symbolu = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.nazwa_symbolu)

class StopienNiepelnosprawnosci(models.Model):
    id_stopnia = models.IntegerField(primary_key=True)
    nazwa_stopnia = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.nazwa_stopnia)

class AktualnySemestr(models.Model):
    id_semestru = models.IntegerField(primary_key=True)
    semestr = models.IntegerField(null=True)

    def __str__(self):
        return str(self.semestr)
    
class SemestrStudenta(models.Model):
    id_semestru = models.IntegerField(primary_key=True)
    semestr = models.IntegerField(null=True)

    def __str__(self):
        return str(self.semestr)

class HistoriaStatusow(models.Model):
    id_statusu = models.AutoField(primary_key=True)
    formularz_id = models.ForeignKey(Formularz, on_delete=models.CASCADE)
    stary_status = models.CharField(max_length=20)
    nowy_status = models.CharField(max_length=20)
    data_zmiany = models.DateTimeField(null=True)

