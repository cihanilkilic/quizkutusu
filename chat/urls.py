from django.urls import path
from . import views
app_name = 'chat' 
urlpatterns = [
    path('', views.ChatView, name='chat_default'),
    path('<str:username>/', views.ChatView, name='chat')
]
