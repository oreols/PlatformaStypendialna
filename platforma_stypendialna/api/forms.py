from django import forms
from .models import Student, Formularz, Osiagniecia
from datetime import datetime



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
        fields = ['liczba_osiagniec', 'student', 'krotki_opis', 'data_osiagniecia']
        widgets = {
            'krotki_opis': forms.Textarea(attrs={'cols': 30, 'rows': 5}), 
        }
