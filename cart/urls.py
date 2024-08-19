from django.urls import path
from .import views

app_name="cart"
urlpatterns = [

    path('cart/', views.cart_add, name='cart_add'),
    # path('cart_show/', views.cart_show, name='cart_show'),
    path('cart_exam_show/', views.cart_exam_show, name='cart_exam_show'),
    path('exam_edit/<str:edit_>/', views.exam_edit, name='exam_edit'),
    path('exam_edit_delete/<int:id>/', views.exam_edit_delete, name='exam_edit_delete'),
    path('exam_delete/<str:delete>/', views.exam_delete, name='exam_delete'),
    path('exam_pdf/<str:e_title>/', views.exam_pdf, name='exam_pdf'),

]
