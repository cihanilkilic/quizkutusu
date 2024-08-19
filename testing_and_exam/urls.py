from django.urls import path
from .import views

app_name="testing_and_exam"
urlpatterns = [
    path('get_elapsed_time/', views.get_elapsed_time, name='get_elapsed_time'),
    path('testing_and_exam/', views.testing_and_exam, name='testing_and_exam'),

    #TESTTİNG URLS
    path('testing/', views.testing, name='testing'),
    path('show_testing/<str:Testing_Name>/', views.show_testing, name='show_testing'),
    path('result_testing/', views.result_testing, name='result_testing'),
    path('testing_result_show/', views.testing_result_show, name='testing_result_show'),
    path('testing_show_result_details/<str:Testing_Name>/', views.testing_show_result_details, name='testing_show_result_details'),
    path('show_testing_istatistic/', views.show_testing_istatistic, name='show_testing_istatistic'),

#-------------------------------------------------------------------------------------------------------------------------------------------# 
    #EXAM URLS
    path('exam_/', views.exam_, name='exam_'),
    path('show_exam_/<str:Exam_Name>/', views.show_exam_, name='show_exam_'),
    path('result_exam/', views.result_exam, name='result_exam'),
    path('exam_result_show/', views.exam_result_show, name='exam_result_show'),
    path('show_exam_result_details/<str:Exam_Name>/', views.show_exam_result_details, name='show_exam_result_details'),
    path('show_exam_istatistic/', views.show_exam_istatistic, name='show_exam_istatistic'),
#-------------------------------------------------------------------------------------------------------------------------------------------# 
    #AYT URLS
    path('ayt/', views.ayt, name='ayt'),
    path('ayt_show/<int:EXAM_Name>/', views.ayt_show, name='ayt_show'),
    path('ayt_result_show/', views.ayt_result_show, name='ayt_result_show'),
    path('ayt_result/', views.ayt_result, name='ayt_result'),
    path('ayt_show_result_details/<str:Date_Choice>/', views.ayt_show_result_details, name='ayt_show_result_details'),
    path('show_ayt_istatistic/', views.show_ayt_istatistic, name='show_ayt_istatistic'),
    


#-------------------------------------------------------------------------------------------------------------------------------------------# 
    #TYT URLS
    path('tyt/', views.tyt, name='tyt'),
    path('show_tyt/<int:EXAM_Name>/', views.show_tyt, name='show_tyt'),
    path('tyt_result_show/', views.tyt_result_show, name='tyt_result_show'),
    path('result_tyt/', views.result_tyt, name='result_tyt'),
    path('show_tyt_result_details/<str:Date_Choice>/', views.show_tyt_result_details, name='show_tyt_result_details'),

    path('show_tyt_istatistic/', views.show_tyt_istatistic, name='show_tyt_istatistic'),
#-------------------------------------------------------------------------------------------------------------------------------------------# 
    #KPSS URLS
     #path('kpss/', views.kpss, name='kpss'),

]
