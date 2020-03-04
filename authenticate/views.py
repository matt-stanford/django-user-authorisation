from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm, EditUserForm

def home(request):
    return render(request, 'home.html', {})


def success(request):
    return render(request, 'success.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('success')
        else:
            messages.success(request, ('Error logging in. Please try again.'))
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out'))
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ('Registration complete.'))
            return redirect('success')

    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


def edit_profile(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, ('Your profile has been updated.'))
            return redirect('home')

    else:
        form = EditUserForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, ('Your password has been updated.'))
            return redirect('home')

    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {'form': form})