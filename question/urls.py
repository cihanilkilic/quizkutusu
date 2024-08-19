from django.urls import path
from .import views

app_name="question"

urlpatterns = [
    path('question/',views.Question_,name="Question"),
    path('get_lessons/', views.get_lessons, name='get_lessons'),
    path('get_topics/', views.get_topics, name='get_topics'),
    path('article_create/',views.article_create,name="article_create"),
    path('question_detail/<int:id>/', views.question_detail, name='question_detail'),
    path('question_delete/', views.question_delete, name='question_delete'),
    path('like_question/', views.like_question, name='like_question'),
     path('get_like_count/',  views.get_like_count, name='get_like_count'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('quiz/', views.quiz, name='quiz'),
    path('save_input_value/', views.save_input_value, name='save_input_value'),
    path('get_exam_titles/', views.get_exam_titles, name='get_exam_titles'),
    
    path('exam_save/', views.exam_save, name='exam_save'),
    path('exam_save_2/', views.exam_save_2, name='exam_save_2'),
    path('exam_save_2_cart_delete//<int:id>/', views.exam_save_2_cart_delete, name='exam_save_2_cart_delete'),
    path('question/<int:question_id>/add_comment/', views.add_comment, name='add_comment'),
    # path('get_topics/', views.get_topics, name='get_topics'),
]
