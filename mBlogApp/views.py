from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegistrationForm

# Create your views here.

def welcome(request):
    return render(request, 'welcome.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(username= form.cleaned_data['username'],
                                     password= form.cleaned_data['password'])
            return redirect('welcome')
    else :
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})    