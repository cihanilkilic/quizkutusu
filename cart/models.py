from django.db import models
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from question.models import Question
from django.contrib import messages
from django.contrib.auth.models import User

# Create your models here.
class Cart(models.Model):
    author=models.ForeignKey(User,on_delete = models.CASCADE,verbose_name="Sepete Ekleyen")
    exam_items=models.IntegerField(null=True,verbose_name="Soru Id:")
    Lessons=models.CharField(verbose_name="Ders Adı",null=True,max_length=50)
    Question=models.TextField(verbose_name="Soru",null=True)
    Choice_A=models.TextField(verbose_name="A Şıkkı",blank=True, null=True)
    Choice_B=models.TextField(verbose_name="B Şıkkı",blank=True, null=True)
    Choice_C=models.TextField(verbose_name="C Şıkkı",blank=True, null=True)
    Choice_D=models.TextField(verbose_name="D Şıkkı",blank=True, null=True)
    Choice_E=models.TextField(verbose_name="E Şıkkı",blank=True, null=True)
    Answer=models.TextField(verbose_name="Cevap",null=True)
    Classroom=models.CharField(verbose_name="Kaçıncı Sınıf Sorusu?",null=True,blank=False,max_length=10)
    Topics_Name=models.CharField(max_length=100,verbose_name="Konu Adı",null=True)
    Question_Types=models.CharField(verbose_name='SORU TİPLERİ',null=True,max_length=20)
    Level = models.CharField(default="KOLAY", max_length=6, blank=True)
    Question_Image=models.ImageField(upload_to='cart_images/',blank=True, null=True, verbose_name="Soruya Fotoğraf Ekleyin")
    created_date=models.DateTimeField(auto_now=True,verbose_name="Oluşturma Tarihi")
    def __str__(self):
        return  'Kullanıcı={0}, Soru Id={1}'.format(self.author, self.exam_items)#self.title,self.content,self.created_date



class CartExamTitle(models.Model):
    author=models.ForeignKey(User,on_delete = models.CASCADE,verbose_name="Sınavı Adını Oluşturan")# bunu django hazır kullanıcı tablosundan alıyoruz
    exam_title=models.CharField(blank=True, max_length=100,verbose_name="Sınav Adı")
    created_date=models.DateTimeField(auto_now=True,verbose_name="Oluşturma Tarihi")

    def __str__(self):
        return  'Kullanıcı={0}, Sınav Adı={1}'.format(self.author, self.exam_title)
    

