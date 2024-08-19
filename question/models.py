from django.db import models
from django.contrib.auth.models import User


class Classroom(models.Model):
    classroom=models.CharField(verbose_name="Kaçıncı Sınıf Öğretmeni?",max_length=15)
    def __str__(self):
        return self.classroom
    class Meta:
        verbose_name_plural = "SINIF EKLEME"


class Lesson(models.Model):
    Classrooms_Name = models.ManyToManyField(Classroom,related_name="lesson_name")
    Lessons_Name=models.CharField(max_length=100,verbose_name="Ders Adı",null=True)

    def __str__(self):
        return self.Lessons_Name
    class Meta:
        verbose_name_plural = "DERS EKLEME"




class Topic(models.Model):
    Lessons_Name = models.ManyToManyField(Lesson,related_name="topics_name")
    Topics_Name=models.CharField(max_length=100,verbose_name="Konu Adı",null=True)

    def __str__(self):
        return self.Topics_Name

    class Meta:
        verbose_name_plural = "KONU EKLEME"


# class Lessons_Topic(models.Model):
#     Topics_Name = models.ForeignKey(Topic,on_delete=models.CASCADE,null=True,related_name="Lessons_Topics_Name")
#     Lessons_Name = models.ForeignKey(Lesson,on_delete=models.CASCADE,null=True,related_name="Lessons_Lessons_Name")
#     Classrooms_Name = models.ForeignKey(Classroom,on_delete=models.CASCADE,null=True,related_name="Classrooms_Lessons_Name")
   

#     def __str__(self):
#         return  'Konu={0}, Ders={1}'.format(self.Topics_Name, self.Lessons_Name)
#         # return  '{0}'.format(self.Topics_Name)






class Question(models.Model):
    author=models.ForeignKey(User,on_delete = models.CASCADE,verbose_name="Soruyu Yazan",related_name="question_author")# bunu django hazır kullanıcı tablosundan alıyoruz
    Lessons=models.CharField(verbose_name="Ders Adı",null=True,max_length=50)
    Question_Image=models.ImageField(upload_to='question_images/',blank=True, null=True, verbose_name="Soruya Fotoğraf Ekleyin")

    Question=models.TextField(verbose_name="Soru")
    Ticket=models.TextField(verbose_name="Çoktan Seçmeli İçin Etiket Adı",blank=True, null=True)
    Cell_1=models.TextField(verbose_name="HÜCRE 1",blank=True, null=True)
    Cell_2=models.TextField(verbose_name="HÜCRE 2",blank=True, null=True)
    Choice_A=models.TextField(verbose_name="A Şıkkı",blank=True, null=True)
    Choice_B=models.TextField(verbose_name="B Şıkkı",blank=True, null=True)
    Choice_C=models.TextField(verbose_name="C Şıkkı",blank=True, null=True)
    Choice_D=models.TextField(verbose_name="D Şıkkı",blank=True, null=True)
    Choice_E=models.TextField(verbose_name="E Şıkkı",blank=True, null=True)

    Answer=models.TextField(verbose_name="Cevap")
    Classroom=models.CharField(verbose_name="Kaçıncı Sınıf Sorusu?",null=True,blank=False,max_length=10)
    Topics_Name=models.CharField(max_length=100,verbose_name="Konu Adı",null=True)
    Question_Types=models.CharField(verbose_name='SORU TİPLERİ',null=True,max_length=20)
    Level = models.CharField(default="KOLAY", max_length=6, blank=True)
    Caption=models.TextField(verbose_name='Açıklama',blank=True, null=True, max_length=150)
    
    Created_Date=models.DateTimeField(auto_now=True,verbose_name="Oluşturma Tarihi")
    
    def author_id(self):
        return self.author,self.Lessons,self.Classroom,self.Topics_Name,self.Question_Types,self.Level
    def __str__(self):
        return  'author={0}, title={1}'.format(self.author, self.Question)#self.title,self.content,self.created_date

    class Meta:
        verbose_name_plural = "SORU EKLEME"


class Comment(models.Model):
    question = models.ForeignKey(Question,on_delete = models.CASCADE,verbose_name="Yorum Yapılan Makale",related_name="comments")#Article Sınıfımız
    comment_author = models.ForeignKey(User,on_delete = models.CASCADE,verbose_name="YORUM YAPAN")#Yorum Yapanın ismi
    comment_content = models.TextField(blank=True, null=True,verbose_name="Yorum")
    created_date = models.DateTimeField(auto_now=True,verbose_name="Oluşturma Tarihi")
    def __str__(self):
         return  'author={0}, title={1}'.format(self.comment_author, self.comment_content)
    class Meta:
        verbose_name_plural = "YORUM EKLEME"

class Like(models.Model):
    author = models.ForeignKey(User,on_delete = models.CASCADE,verbose_name="SORUYU BEĞENEN")
    question = models.ForeignKey(Question,on_delete = models.CASCADE,verbose_name="BEĞENİ YAPILAN SORU",related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('author', 'question')
    def __str__(self):
         return  'KULLANICI={0}, SORU={1}'.format(self.author, self.question)

    class Meta:
        verbose_name_plural = "BEĞENME İŞLEMİ"