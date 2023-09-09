from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

# TODO: add a forgot account/forgot details option

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})