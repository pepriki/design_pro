
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, DesignRequestForm
from .models import DesignRequest


def home(request):
    return render(request, 'main/home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(request, 'Регистрация успешно завершена!')
            return redirect('my_requests')
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, 'Вы успешно вошли в аккаунт.')
            return redirect('my_requests')
    else:
        form = AuthenticationForm(request)

    return render(request, 'main/login.html', {'form': form})


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Вы вышли из аккаунта.')

    return redirect('home')


@login_required(login_url='login')
def my_requests(request):
    user_requests = DesignRequest.objects.filter(user=request.user)

    selected_status = request.GET.get('status', '')

    if selected_status in dict(DesignRequest.STATUS_CHOICES):
        user_requests = user_requests.filter(status=selected_status)
    else:
        selected_status = ''

    context = {
        'requests': user_requests,
        'statuses': DesignRequest.STATUS_CHOICES,
        'selected_status': selected_status,
    }

    return render(request, 'main/my_requests.html', context)


@login_required(login_url='login')
def create_request(request):
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)

        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.user = request.user
            new_request.save()

            messages.success(request, 'Заявка успешно создана!')
            return redirect('my_requests')
    else:
        form = DesignRequestForm()

    return render(request, 'main/create_request.html', {
        'form': form
    })

@login_required(login_url='login')
def delete_request(request, request_id):
    if request.method == 'POST':
        design_request = get_object_or_404(
            DesignRequest,
            id=request_id,
            user=request.user
        )

        if design_request.status == 'new':
            design_request.delete()
            messages.success(request, 'Заявка успешно удалена.')
        else:
            messages.error(
                request,
                'Можно удалять только новые заявки.'
            )

    return redirect('my_requests')