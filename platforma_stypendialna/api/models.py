from django.db import models

class Kierunek(models.Model):
    id_kierunku = models.IntegerField(primary_key=True)
    nazwa_kierunku = models.TextField(null=True)

    def __str__(self):
        return self.nazwa_kierunku

class DecyzjeStypendialne(models.Model):
    id_decyzji = models.IntegerField(primary_key=True)
    id_student = models.IntegerField(null=True)
    decyzja = models.SmallIntegerField(null=True)

class Formularz(models.Model):
    id_formularza = models.IntegerField(primary_key=True)
    typ_stypendium = models.TextField(null=True)
    id_student = models.IntegerField(null=True)
    data_zlozenia = models.DateField(null=True)
    przychod_bez_podatku = models.FloatField(null=True)
    srednia_ocen = models.FloatField(null=True)
    dodatkowe_informacje = models.TextField(null=True)
    plik_orzeczenie = models.CharField(max_length=45, null=True)
    id_osiagniecia = models.IntegerField(null=True)
    oswiadczenie_prawo_o_szkolnictwie = models.BooleanField(default=False)
    oswiadczenie_gospodarstwo_domowe = models.BooleanField(default=False)
    oswiadczenie_dochody = models.BooleanField(default=False)
    zalacznik = models.TextField(null=True)
    stopien_niepelnosprawnosci = models.TextField(null=True)
    charakter_stopnia_niepelnosprawnosci = models.TextField(null=True)
    data_rozpoczecia_orzeczenia = models.DateField(null=True)
    data_konca_orzeczenia = models.DateField(null=True)

class Student(models.Model):
    id_student = models.IntegerField(primary_key=True)
    nazwa_uzytkownika = models.TextField(null=True)
    haslo = models.TextField(null=True)
    email = models.TextField(null=True)
    data_rejestracji = models.DateField(null=True)
    ikonka = models.TextField(null=True)
    pesel = models.TextField(null=True)
    imie = models.TextField(null=True)
    nazwisko = models.TextField(null=True)
    numer_telefonu = models.TextField(null=True)
    nazwa_kierunku = models.TextField(null=True)
    semestr = models.IntegerField(null=True)
    numer_albumu = models.IntegerField(null=True)
    rok_studiow = models.IntegerField(null=True)
    kierunek = models.ForeignKey(Kierunek, on_delete=models.CASCADE)
    decyzjeStypendialne = models.ForeignKey(DecyzjeStypendialne, on_delete=models.CASCADE)
    ##formularz = models.ForeignKey(Formularz, blank=True, null = True, on_delete=models.CASCADE)
    numer_konta_bankowego = models.TextField(null=True)

    def __str__(self):
        return self.nazwa_uzytkownika

class Admin(models.Model):
    id_admin = models.IntegerField(primary_key=True)
    haslo = models.TextField(null=True)
    login = models.TextField(null=True)
    email = models.TextField(null=True)

class Aktualnosci(models.Model):
    id_aktualnosci = models.IntegerField(primary_key=True)
    nazwa_aktualnosci = models.TextField(null=True)
    tekst_aktualnosci = models.TextField(null=True)
    data_opublikowania = models.DateField(null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)

class Kontakt(models.Model):
    id_kontakt = models.IntegerField(primary_key=True)
    email = models.TextField(null=True)
    numer_tel = models.IntegerField(null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)

class Przedmiot(models.Model):
    id_przedmiot = models.IntegerField(primary_key=True)
    nazwa_przedmiotu = models.TextField(null=True)
    id_kierunku = models.IntegerField(null=True)
    semestr = models.IntegerField(null=True)
    kierunek = models.ForeignKey(Kierunek, on_delete=models.CASCADE)
    punkty_ects = models.IntegerField(null=True)

class OcenaKoncowa(models.Model):
    id_ocena = models.IntegerField(primary_key=True)
    id_student = models.IntegerField(null=True)
    ocena_koncowa = models.FloatField(null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    id_przedmiotu = models.IntegerField(null=True)
    przedmiot = models.ForeignKey(Przedmiot, on_delete=models.CASCADE)

class Kryteria(models.Model):
    rok_kryterium = models.IntegerField(primary_key=True)
    srednia_ocen = models.FloatField(null=True)
    przychod_bez_podatku = models.FloatField(null=True)
    id_kierunku = models.IntegerField(null=True)
    id_formularza = models.IntegerField(null=True)
    wzor_stypendium = models.TextField(null=True)
    formularz = models.ForeignKey(Formularz, on_delete=models.CASCADE)

class Ustawienia(models.Model):
    id_student = models.IntegerField(primary_key=True)
    nowe_haslo = models.TextField(null=True)
    nowy_numer_konta_bankowego = models.TextField(null=True)
    nowy_email = models.TextField(null=True)
    nowe_imie = models.TextField(null=True)
    nowe_nazwisko = models.TextField(null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE) 

class Ranking(models.Model):
    numer_albumu = models.IntegerField(primary_key=True)
    punkty_rankingu = models.CharField(max_length=45, null=True)
    typ_stypendium = models.CharField(max_length=65, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

class DaneDziekanat(models.Model):
    numer_albumu = models.IntegerField(primary_key=True)
    ocena_koncowa = models.FloatField(null=True)
    imie = models.TextField(null=True)
    nazwisko = models.TextField(null=True)
    pesel = models.TextField(null=True)
    srednia_ocen = models.FloatField(null=True)
    id_przedmiot = models.IntegerField(null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    id_kierunku = models.IntegerField(null=True)

class Powiadomienia(models.Model):
    id_powiadomienia = models.IntegerField(primary_key=True)
    tresc_powiadomienia = models.TextField(null=True)
    naglowek_powiadomienia = models.TextField(null=True)
    autor_powiadomienia = models.TextField(null=True)
    student_id_powiadomienie = models.IntegerField(null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

class KryteriaStrona(models.Model):
    id_wersja = models.IntegerField(primary_key=True)
    rok = models.TextField(null=True)
    tekst = models.TextField(null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)

class InformacjeStypendialne(models.Model):
    id_wersja = models.IntegerField(primary_key=True)
    tekst = models.TextField(null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)

class StudentLog(models.Model):
    id_log = models.IntegerField(primary_key=True)
    adres_ip = models.CharField(max_length=45, null=True)
    nazwa_uzytkownika = models.TextField(null=True)
    haslo = models.TextField(null=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)

class AdminLog(models.Model):
    id_log_admin = models.IntegerField(primary_key=True)
    adres_ip = models.TextField(null=True)
    login = models.TextField(null=True)
    haslo = models.TextField(null=True)

class Konkursy(models.Model):
    id_konkursu = models.IntegerField(primary_key=True)
    nazwa_konkursu = models.TextField(null=True)
    nazwa_kierunku = models.ForeignKey(Kierunek, on_delete=models.CASCADE)

class Osiagniecia(models.Model):
    id_osiagniecia = models.IntegerField(primary_key=True)
    id_konkursu = models.IntegerField(null=True)
    id_student = models.IntegerField(null=True)
    punkty_osiagniecie = models.IntegerField(null=True)
    typ_osiagniecia = models.TextField(null=True)
    konkursy = models.ForeignKey('Konkursy', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    krotki_opis = models.TextField(null=True)
    data_osiagniecia = models.DateField(null=True)

class OcenaKoncowaDziekanat(models.Model):
    id_ocena = models.IntegerField(primary_key=True)
    numer_albumu = models.IntegerField(null=True)
    ocena_koncowa = models.FloatField(null=True)
    id_przedmiotu = models.IntegerField(null=True)
    dane_dziekanat = models.ForeignKey('DaneDziekanat', on_delete=models.CASCADE)
    przedmiot = models.ForeignKey('Przedmiot', on_delete=models.CASCADE)
    
class CzlonekRodziny(models.Model):
    id_czlonka = models.IntegerField(primary_key=True)
    imie_czlonka = models.TextField(null=True)
    nazwisko_czlonka = models.TextField(null=True)
    stopien_pokrewienstwa = models.IntegerField(null=True)
    data_urodzenia = models.DateTimeField(null=True)
    miejsce_pracy = models.TextField(null=True)
    formularz = models.ForeignKey('Formularz', on_delete=models.CASCADE)
