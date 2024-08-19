from django.urls import path
from .import views

app_name = 'quizbox'
urlpatterns = [
    path('',views.index,name="index"),
    path('search/',views.search_questions, name='search_questions'),

]
