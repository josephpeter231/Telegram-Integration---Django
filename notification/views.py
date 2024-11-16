from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .slack_utils import send_slack_message
import socket

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Send Slack message
            send_slack_message(f"New user registered: {user.username}")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# User Login View
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Get user details and IP
            ip_address = request.META.get('REMOTE_ADDR', '')
            hostname = socket.gethostname()
            message = f"User {user.username} logged in from IP: {ip_address}, Hostname: {hostname}"
            send_slack_message(message)
            return redirect('home')
        else:
            return HttpResponse('Invalid login credentials')
    return render(request, 'login.html')

# Home View
def home(request):
    return render(request, 'home.html', {'username': request.user.username})
