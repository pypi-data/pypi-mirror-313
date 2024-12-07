from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
class Authentication:
    @staticmethod
    def get_signup(request):
        if request.method == 'GET':
            return render(request, 'signup.html', {
                'form': UserCreationForm()
            })
        elif request.method == 'POST':
            if request.POST['password1'] == request.POST['password2']:
                try:
                    # Register user\n"
                    user = User.objects.create_user(
                        username=request.POST['username'], password=request.POST['password2'])
                    user.save()
                    login(request, user)
                    return redirect('logged')
                except IntegrityError:
                    return render(request, 'signup.html', {
                        'form': UserCreationForm(),
                        'error': 'User already exists'
                    })
            return render(request, 'signup.html', {
                'form': UserCreationForm(),
                'error': 'Passwords do not match'
            })
    @staticmethod
    def get_signout(request):
        logout(request)
        return redirect('home')
    @staticmethod
    def get_signing(request):
        if request.method == 'GET':
            return render(request, 'login.html', {
                'form': AuthenticationForm,
            })
        elif request.method == 'POST':
            try:
                User.objects.get(username=request.POST['username'])
            except User.DoesNotExist:
                return render(request, 'login.html', {
                    'form': AuthenticationForm,
                    'error': 'User does not exist in the database'
                })
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request, 'login.html', {
                    'form': AuthenticationForm,
                    'error': 'username or password is incorrect'
                })
            else:
                login(request, user)
                return redirect('logged')
    @staticmethod
    def get_logged(request):
        return render(request, 'logged.html')
    def dispatch(self, request, *args, **kwargs):
        match request.path:
            case "/signup":
                return self.get_signup(request)
            case "/login":
                return self.get_signing(request)
            case "/logout":
                return self.get_signout(request)
            case "/logged":
                return self.get_logged(request)
            case "/":
                return self.get(request)
            case _:
                return self.get(request)