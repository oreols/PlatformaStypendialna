from django.db import models

class Kierunek(models.Model):
    id_kierunku = models.IntegerField(primary_key=True)
    nazwa_kierunku = models.TextField(null=True)

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

