from django.shortcuts import render
from django.http import HttpResponse;
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def main(request):
    return HttpResponse("Witam na platformie stypendialnej!")

def loginPage(request):
    return HttpResponse("Strona logowania")

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'register.html', context)