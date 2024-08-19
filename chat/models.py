from django.db import models
from django.contrib.auth.models import User  # Varsayılan Django kullanıcı modeli
from django.utils import timezone



class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=10, default='text')

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.message}"