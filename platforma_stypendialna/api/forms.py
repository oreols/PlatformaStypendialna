from django import forms
from .models import Student

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
