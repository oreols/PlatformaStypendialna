from django import forms
from .models import Student, Formularz, Osiagniecia, Kontakt, Aktualnosci, CzlonekRodziny
from datetime import datetime
from django.core.exceptions import ValidationError



class StudentRegistrationForm(forms.ModelForm):
    
    email = forms.EmailField()
    data_rejestracji = forms.DateField(initial=datetime.now())

    class Meta:
        model = Student
        fields = ['username', 'password', 'email', 'data_rejestracji', 'pesel', 'imie', 'nazwisko', 'numer_telefonu', 'semestr', 'numer_albumu', 'rok_studiow', 'nazwa_kierunku', 'numer_konta_bankowego', 'zalaczniki']
        widgets = {
            'password': forms.PasswordInput()  
        }

    def __init__(self, *args, **kwargs):
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        # You can customize form fields here if needed

    def clean_data_rejestracji(self):
        data_rejestracji = self.cleaned_data.get('data_rejestracji')
        if data_rejestracji is None or data_rejestracji < datetime.now().date():
            data_rejestracji = datetime.now()  # Zastąp datę starszą dzisiejszą datą
        return data_rejestracji
        
    def clean_numer_albumu(self, *args, **kwargs):
        numer_albumu = self.cleaned_data.get('numer_albumu')
        if len(numer_albumu) == 5:
            return numer_albumu
        else:
            raise forms.ValidationError('Niepoprawny numer albumu')
        
    def clean_semestr(self, *args, **kwargs):
        semestr = self.cleaned_data.get('semestr')
        if len(semestr) == 1 and (semestr == '1' or semestr == '2'):
            return semestr
        else:
            raise forms.ValidationError('Wpisz 1 lub 2')
        
    def clean_rok_studiow(self, *args, **kwargs):
        rok_studiow = self.cleaned_data.get('rok_studiow')
        if len(rok_studiow) == 1 and (rok_studiow == '1' or rok_studiow == '2' or rok_studiow == '3' or rok_studiow == '4' or rok_studiow == '5'):
            return rok_studiow
        else:
            raise forms.ValidationError('Wpisz od 1 do 5')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Student.objects.filter(email=email).exists():
            raise forms.ValidationError('Email jest już zajęty')
        return email
        
class SkladanieFormularzaDlaNiepelnosprawnych(forms.ModelForm):
    
    class Meta:
        model = Formularz
        fields = ['typ_stypendium', 'data_zlozenia', 'stopien_niepelnosprawnosci', 'symbol_niepelnosprawnosci', 'charakter_stopnia_niepelnosprawnosci', 'data_rozpoczecia_orzeczenia','data_konca_orzeczenia', 'aktualny_semestr', 'semestr_studenta', 'zalacznik_niepelnosprawnosc']

    def clean_data_zlozenia(self):
        data_zlozenia = datetime.now()  # Zastąp datę starszą dzisiejszą datą
        return data_zlozenia 
 

    # def __init__(self, *args, **kwargs):
    #     super(SkladanieFormularzaDlaNiepelnosprawnych, self).__init__(*args, **kwargs)
        # You can customize form fields here if needed

class SkladanieFormularzaNaukowego(forms.ModelForm):
    
    class Meta:
        model = Formularz
        fields = ['typ_stypendium', 'data_zlozenia', 'srednia_ocen', 'aktualny_semestr', 'semestr_studenta', 'zalacznik']
    
    def clean_data_zlozenia(self):
        data_zlozenia = datetime.now()  # Zastąp datę starszą dzisiejszą datą
        return data_zlozenia 
    
class ZapiszOsiagniecie(forms.ModelForm):

    class Meta:
        model = Osiagniecia 
        fields = ['liczba_osiagniec', 'krotki_opis', 'data_osiagniecia']
        
        widgets = {
            'krotki_opis': forms.Textarea(attrs={'cols': 30, 'rows': 5}), 
        }
def validate_tel(value):
    if len(value) != 9:
        raise ValidationError("Numer telefonu musi składać się z 9 cyfr")
def validate_email(value):
    if '@' not in value:
        raise ValidationError("Niepoprawny adres email")
 

class KontaktForm(forms.ModelForm):
    numer_tel = forms.CharField(validators=[validate_tel])
    email = forms.EmailField(validators=[validate_email])
    class Meta:
        model = Kontakt
        fields = ['email','numer_tel']
        widgets = {
            'email': forms.EmailInput(attrs={'width': '250px'}),
            'numer_tel': forms.TextInput(attrs={'placeholder': 'np. 123456789', 'width': '100px'})
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email == '':
            raise forms.ValidationError('To pole nie może być puste')
        if '@' not in email:
            raise forms.ValidationError('Niepoprawny format adresu email')
        return email
    def clean_numer_tel(self):
        numer_tel = self.cleaned_data.get('numer_tel')
        if len(numer_tel) < 9 or len(numer_tel) > 9:
            raise forms.ValidationError('Niepoprawny numer telefonu')
        return numer_tel
    
class AktualnosciForm(forms.ModelForm):
    class Meta:
        model = Aktualnosci
        fields = ['nazwa_aktualnosci', 'tekst_aktualnosci', 'data_opublikowania']
        widgets = {
            'nazwa_aktualnosci': forms.TextInput(attrs={'width': '250px'}),
            'tekst_aktualnosci': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
            'data_opublikowania': forms.DateInput(attrs={'type': 'date'})
        }
    def clean_data_opublikowania(self):
        data_opublikowania = datetime.now()
        return data_opublikowania
    
class FormularzSocjalne(forms.ModelForm):
    class Meta:
        model = Formularz
        fields = ['typ_stypendium', 'data_zlozenia', 'oswiadczenie_dochody', 'przychod_bez_podatku', 'oswiadczenie_prawo_o_szkolnictwie', 'oswiadczenie_gospodarstwo_domowe', 'aktualny_semestr', 'semestr_studenta', 'zalacznik']
        widgets = {
            'oswiadczenie_prawo_o_szkolnictwie': forms.RadioSelect(),
            'oswiadczenie_gospodarstwo_domowe': forms.RadioSelect(),
            'oswiadczenie_dochody': forms.RadioSelect(),
        }
    
    def clean_data_zlozenia(self):
        data_zlozenia = datetime.now()
        self.cleaned_data['data_zlozenia'] = data_zlozenia
        return data_zlozenia
    
    def clean_typ_stypendium(self):
        typ_stypendium = "socjalne"
        return typ_stypendium

class CzlonekSocjalne(forms.ModelForm):
    class Meta:
        model = CzlonekRodziny
        fields = ['imie_czlonka', 'nazwisko_czlonka', 'data_urodzenia', 'stopien_pokrewienstwa', 'miejsce_pracy']
        widgets = {
            'imie_czlonka': forms.TextInput(attrs={'width': '150px'}),
            'nazwisko_czlonka': forms.TextInput(attrs={'width': '150px'}),
            'stopien_pokrewienstwa': forms.TextInput(attrs={'width': '150px'}),
            'miejsce_pracy': forms.TextInput(attrs={'width': '150px'}),
            'data_urodzenia': forms.DateInput(attrs={'type': 'date'})
        }