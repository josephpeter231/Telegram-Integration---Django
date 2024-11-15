import asyncio
import aiohttp
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import socket
from requests.exceptions import RequestException

# Asynchronous Function to send a message to Telegram
async def send_telegram_message(message):
    token = 'yourtoken'
    chat_id ="enter your chat id"
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message,
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()  # Raise an exception for 4xx/5xx responses
                if response.status == 200:
                    print("Message sent successfully!")
                else:
                    print(f"Error sending message: {response.status}")
        except Exception as e:
            print(f"Error sending Telegram message: {e}")

# Function to run the async send message function
def run_send_telegram_message(message):
    asyncio.run(send_telegram_message(message))

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
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
            
            # Get user info
            ip_address = request.META.get('REMOTE_ADDR', '')
            hostname = socket.gethostname()
            location = "Unknown"  
            
            message = f"User {user.username} logged in. IP: {ip_address}, Location: {location}"
            run_send_telegram_message(message)
            
            return redirect('home')
        else:
            return HttpResponse('Invalid login credentials')
    return render(request, 'login.html')

# Home page for logged-in users
@login_required
def home(request):
    return HttpResponse(f"Welcome, {request.user.username}!")
