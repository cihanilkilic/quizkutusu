from django.urls import path
from . import views
app_name="user"
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/', views.User_Login, name ='User_Login'),
    path('logout/',views.User_Logout,name="User_Logout"),

    path('register/',views.User_Register, name ='User_Register'),  
    path('activate<uidb64>/<token>/', views.activate, name='activate'),  

    path('user/<int:pk>/',views.user_subscribe_edit,name='user_subscribe_edit'),

    path('profil/<int:pk>/',views.User_Profil,name="User_Profil"),
    path('student_works/',views.student_works,name="student_works"),
    path('follow/',views.followView, name="followView"),    
    path('teacher_profiles/',views.teacher_profiles, name="teacher_profiles"),    
    path('profile_question_delete/<int:pk>/',views.profile_question_delete, name="profile_question_delete"),    

    #path('profil/<int:id>/',views.User_Profil,name="Profil"),
    # path('User_Info_Save/',views.User_Info_Save,name="User_Info_Save"),
    path('User_Info_Update/<int:pk>/',views.User_Info_Update,name="User_Info_Update"),

       # Şifre sıfırlama URL'leri
    path('password-reset/',  views.password_reset_request, name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/',  views.password_reset_confirm, name='password_reset_confirm'),
    
]