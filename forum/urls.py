from django.urls import path
from .import views

app_name="forum"
urlpatterns = [

    path('forum_create/', views.forum_create, name='forum_create'),
    path('forum_comment_create/', views.forum_comment_create, name='forum_comment_create'),
    path('forum_comment_list/', views.forum_comment_list, name='forum_comment_list'),
    path('discover/',views.discover, name='discover'),
    path('discover/forum/search_forum/', views.search_forum, name='search_forum'),
    path('forum_detail/<int:pk>/', views.forum_detail, name='forum_detail'),
    path('get_like_count/',  views.get_like_count, name='get_like_count'),
    path('like_forum/', views.like_forum, name='like_forum'),


]
