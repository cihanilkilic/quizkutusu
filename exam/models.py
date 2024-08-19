from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Exam(models.Model):
    author=models.ForeignKey(User,on_delete = models.CASCADE,verbose_name="Soruyu Yazan",default=0)# bunu django hazır kullanıcı tablosundan alıyoruz
    Lessons=models.CharField(verbose_name="Ders Adı",null=True,max_length=50,default=0)
    Exam_Title=models.CharField(verbose_name="Sınav Adı",null=True,max_length=50,default=0)
    Question=models.TextField(verbose_name="Soru",blank=True, null=True)
    Choice_A=models.TextField(verbose_name="A Şıkkı",blank=True, null=True)
    Choice_B=models.TextField(verbose_name="B Şıkkı",blank=True, null=True)
    Choice_C=models.TextField(verbose_name="C Şıkkı",blank=True, null=True)
    Choice_D=models.TextField(verbose_name="D Şıkkı",blank=True, null=True)
    Choice_E=models.TextField(verbose_name="E Şıkkı",blank=True, null=True)
    Answer=models.TextField(verbose_name="Cevap",blank=True, null=True)
    Classroom=models.CharField(verbose_name="Kaçıncı Sınıf Sorusu?",null=True,blank=False,max_length=10,default=0)
    Topics_Name=models.CharField(max_length=100,verbose_name="Konu Adı",null=True,default=0)
    Question_Types=models.CharField(verbose_name='SORU TİPLERİ',null=True,max_length=20,default=0)
    Level = models.CharField(max_length=6, blank=True,default=0)
    Question_ID = models.CharField(max_length=30, blank=True,default=0)
    Question_Image=models.ImageField(upload_to='question_images/',blank=True, null=True, verbose_name="Soruya Fotoğraf Ekleyin")
    Created_Date=models.DateTimeField(auto_now=True,verbose_name="Oluşturma Tarihi")

    def author_id(self):
        return self.author
    def __str__(self):
        return  'author={0}, title={1}'.format(self.author, self.Question)#self.title,self.content,self.created_date


