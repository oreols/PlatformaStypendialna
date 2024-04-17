from django import forms
from .models import Student, Formularz
from datetime import datetime


class StudentRegistrationForm(forms.ModelForm):
    
    email = forms.EmailField()
    data_rejestracji = forms.DateField(initial=datetime.now())

    class Meta:
        model = Student
        fields = ['nazwa_uzytkownika', 'password', 'email', 'data_rejestracji', 'pesel', 'imie', 'nazwisko', 'numer_telefonu', 'semestr', 'numer_albumu', 'rok_studiow', 'kierunek', 'numer_konta_bankowego', 'zalaczniki']
        widgets = {
            'password': forms.PasswordInput()  
        }

    def clean_data_rejestracji(self):
        data_rejestracji = self.cleaned_data.get('data_rejestracji')
        if data_rejestracji is None or data_rejestracji < datetime.now().date():
            data_rejestracji = datetime.now()  # Zastąp datę starszą dzisiejszą datą
        return data_rejestracji
    

    def __init__(self, *args, **kwargs):
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        # You can customize form fields here if needed


    def clean_numer_telefonu(self, *args, **kwargs):
        numer_telefonu = self.cleaned_data.get('numer_telefonu')
        if '1' in numer_telefonu:
            return numer_telefonu
        else:
            raise forms.ValidationError('Niepoprawny numer telefonu')
        
class SkladanieFormularzaDlaNiepelnosprawnych(forms.ModelForm):
    
    class Meta:
        model = Formularz
        typ_stypendium = forms.CharField(initial='dla niepełnosprawnych') 
        fields = ['typ_stypendium', 'data_zlozenia', 'stopien_niepelnosprawnosci', 'symbol_niepelnosprawnosci', 'charakter_stopnia_niepelnosprawnosci', 'data_rozpoczecia_orzeczenia','data_konca_orzeczenia', 'aktualny_semestr', 'semestr_studenta', 'zalacznik_niepelnosprawnosc']
        

    #def __init__(self, *args, **kwargs):
        #super(SkladanieFormularzaForm, self).__init__(*args, **kwargs)
        # You can customize form fields here if needed
