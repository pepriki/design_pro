from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegisterForm

def home(request):
    return render(request, 'main/home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                'Регистрация успешно завершена!'
            )
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {'form': form})
