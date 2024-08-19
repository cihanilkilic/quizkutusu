from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Message
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def ChatView(request, username=None):
    if username:
        recipient = get_object_or_404(User, username=username)
    else:
        recipient = None  # veya varsayılan bir değer

    # Eğer recipient varsa, mesajları al
    if recipient:
        messages = Message.objects.filter(
            sender=request.user,
            recipient=recipient
        ).union(
            Message.objects.filter(
                sender=recipient,
                recipient=request.user
            )
        ).order_by('created_at')
    else:
        messages = []

    current_user = request.user
    users = User.objects.exclude(id=current_user.id)
    
    context = {
        'recipient': recipient,
        'messages': messages,
        'users': users
    }
    
    return render(request, 'chat/chat.html', context)