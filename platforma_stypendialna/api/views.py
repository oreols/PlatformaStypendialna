from django.shortcuts import redirect, render
from django.http import HttpResponse;
from django.contrib.auth.forms import UserCreationForm

from .forms import StudentRegistrationForm
# Create your views here.

def main(request):
    return HttpResponse("Witam na platformie stypendialnej!")

def loginPage(request):
    return HttpResponse("Strona logowania")

def registerPage(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = StudentRegistrationForm()
    return render(request, 'rejestracja.html', {'form': form})