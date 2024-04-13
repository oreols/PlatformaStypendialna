from django import forms
from .models import Student, Formularz

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['nazwa_uzytkownika', 'haslo', 'email', 'data_rejestracji', 'pesel', 'imie', 'nazwisko', 'numer_telefonu', 'semestr', 'numer_albumu', 'rok_studiow', 'kierunek', 'numer_konta_bankowego', 'zalaczniki']
        widgets = {
            'haslo': forms.PasswordInput()  # Render the password field as a password input
        }

    def __init__(self, *args, **kwargs):
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        # You can customize form fields here if needed
class SkladanieFormularzaDlaNiepelnosprawnych(forms.ModelForm):
    
    class Meta:
        model = Formularz
        typ_stypendium = forms.CharField(initial='dla niepełnosprawnych') 
        fields = ['typ_stypendium', 'data_zlozenia', 'stopien_niepelnosprawnosci', 'symbol_niepelnosprawnosci', 'charakter_stopnia_niepelnosprawnosci', 'data_rozpoczecia_orzeczenia','data_konca_orzeczenia', 'aktualny_semestr', 'semestr_studenta', 'zalacznik_niepelnosprawnosc']
        

    #def __init__(self, *args, **kwargs):
        #super(SkladanieFormularzaForm, self).__init__(*args, **kwargs)
        # You can customize form fields here if needed
