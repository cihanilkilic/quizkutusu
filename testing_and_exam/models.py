from django.db import models

from django.contrib.auth.models import User




class Question_Choice(models.Model):
    Lessons_Name  = (
        ('Türk Dili ve Edebiyatı', 'Türk Dili ve Edebiyatı'),
        ('Matematik', 'Matematik'),
        ('Fizik', 'Fizik'),
        ('Kimya','Kimya'),
        ('Tarih','Tarih'),
        ('Biyoloji','Biyoloji'),
        ('Coğrafya','Coğrafya'),
        ('Din Kültürü ve Ahlak Bilgisi','Din Kültürü ve Ahlak Bilgisi')
    )

    Answer_Choice  = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D','D'),
        ('E','E')
    )
    Class_Choice  = (
        ('9. Sınıf', '9. Sınıf'),
        ('10. Sınıf', '10. Sınıf'),
        ('11. Sınıf', '11. Sınıf'),
        ('12. Sınıf','12. Sınıf')
    )
    Period_Name  = (
        ('1. Dönem', '1. Dönem'),
        ('2. Dönem', '2. Dönem')

    )
    author=models.ForeignKey(User,on_delete = models.CASCADE,verbose_name="SORUYU YAZAN")# bunu django hazır kullanıcı tablosundan alıyoruz
    Class_Choice=models.CharField(verbose_name="KAIÇINCI SINIF SORUSU ?",choices=Class_Choice,null=True,blank=False,max_length=15)
    Lessons_Name = models.CharField(verbose_name="DERS ADI", choices=Lessons_Name, max_length=100, blank=False)
    Period_Name=models.CharField(verbose_name="DÖNEM ADI ?",choices=Period_Name, max_length=13, blank=False)
    Exam_Name=models.TextField(verbose_name="SINAV ADI",blank=True, null=True,max_length=100)
    sinavi_cozen_kisi=models.ManyToManyField(User,default=None,related_name="sinavi_cozen_kisi",verbose_name="sinavi_cozen_kisi",blank=True, null=True,max_length=100)
    Question=models.TextField(verbose_name="SORU")
    Choice_A=models.TextField(verbose_name="A ŞIKKI",blank=True, null=True)
    Choice_B=models.TextField(verbose_name="B ŞIKKI",blank=True, null=True)
    Choice_C=models.TextField(verbose_name="C ŞIKKI",blank=True, null=True)
    Choice_D=models.TextField(verbose_name="D ŞIKKI",blank=True, null=True)
    Choice_E=models.TextField(verbose_name="E ŞIKKI",blank=True, null=True)
    # hour_s = models.PositiveSmallIntegerField(verbose_name="SAAT:",default=0,blank=True, null=True)  # Saati temsil etmek için
    # minute_s = models.PositiveSmallIntegerField(verbose_name="DAKİKA:",default=0,blank=True, null=True)  # Dakikayı temsil etmek için
    Answer_Choice=models.CharField(verbose_name="CEVAP", choices=Answer_Choice, max_length=1, blank=False)
    Question_Image=models.ImageField(upload_to='testing_and_exam_images/',blank=True, null=True, verbose_name="SORUYA FOTOĞRAF EKLEYİN")
    Created_Date=models.DateTimeField(auto_now=True,verbose_name="OLUŞTURMA TARİHİ")


    def __str__(self):
        #return f"{self.Lessons_Name},{self.Period_Name},{self.Exam_Name},{self.id}"
        return  'SINAVI HAZIRLAYAN={0},SINAV ADI={1}, SORU ID={2}, CEVAP ANAHTARI={3}'.format(
                    self.author, 
                    self.Exam_Name,
                    self.id,
                    self.Answer_Choice,
                    )


    def __str__(self):
        #return f"{self.Lessons_Name},{self.Period_Name},{self.Exam_Name},{self.id}"
        return  self.Exam_Name

    class Meta:
        verbose_name_plural = "(TEKİL) SINAV SORU EKLEME"






class Exam_Result(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="CEVAP VEREN")
    Exam_Name = models.CharField(max_length=100, verbose_name="SINAV ADI", blank=True, null=True)
    Question_Id = models.IntegerField(verbose_name="SORU ID", blank=True, null=True)
    #Question_Id = models.CharField(max_length=110, verbose_name="SORU ID", blank=True, null=True)
    Question_Key = models.CharField(max_length=1, verbose_name="SORUNUN CEVAP ANAHTARI", blank=True, null=True)
    author_Key = models.CharField(max_length=1, verbose_name="CEVAP VERİLEN ŞIK", blank=False)
    True_Answer = models.CharField(max_length=1, default=2, verbose_name="CEVAP DOĞRU MU? ('0 => Yanlış, 1 => Doğru, 2 => Boş')", blank=True, null=True)

    def __str__(self):
        return 'SINAVA KATILAN={0}, SINAV ADI={1}, SORU ID={2}, CEVAP ANAHTARI={3}, SORUYA VERİLEN CEVAP={4}, SORUYU DOĞRU MU YAPTI?={5}'.format(
            self.author,
            self.Exam_Name,
            self.Question_Id,
            self.Question_Key,
            self.author_Key,
            self.True_Answer,
        )

    class Meta:
        verbose_name_plural = "(TEKİL) SINAV SONUÇLARI"



class Exam_Table(models.Model):
    author=models.ForeignKey(User,on_delete = models.CASCADE,verbose_name="SINAVA KATILAN")# bunu django hazır kullanıcı tablosundan alıyoruz
    Exam_Name = models.CharField(max_length=100, verbose_name="SINAV ADI", blank=True, null=True)
    Total_Number_Of_Questions=models.CharField(max_length=3,verbose_name="TOPLAM SORU SAYISI", blank=True, null=True)
    Number_Of_True=models.CharField(max_length=3,verbose_name="TOPLAM DOĞRU SAYISI", blank=True, null=True)
    Number_Of_False=models.CharField(max_length=3,verbose_name="TOPLAM YANLIŞ SAYISI", blank=True, null=True)
    Number_Of_Empty=models.CharField(max_length=3,verbose_name="TOPLAM BOŞ SAYISI", blank=True, null=True)
    Exam_Score = models.CharField(max_length=3,verbose_name="SINAVDAN ALDIĞI PUAN", blank=True, null=True)
    Exam_Rating = models.CharField(max_length=3,verbose_name="SINAV DERECESİ", blank=True, null=True)
    Completion_Time = models.CharField(max_length=50,verbose_name="SINAV BİTİRME SÜRESİ", blank=True, null=True)
    Exam_Date = models.DateTimeField(auto_now=False,verbose_name="SINAV BİTİRME TARİHİ")



    def __str__(self):
        return 'SINAV BİTİRME TARİHİ={0}'.format(
        self.Exam_Date
        )

    class Meta:
        verbose_name_plural = "(TEKİL) SINAV TABLOSU"

# from django.core.exceptions import ValidationError

# class TIMER_S(models.Model):
#     author=models.ForeignKey("user.Profile",on_delete = models.CASCADE,verbose_name="SINAV SÜRESİNİ YAZAN KİŞİ")# bunu django hazır kullanıcı tablosundan alıyoruz
#     Exam_Name=models.TextField(verbose_name="SINAV ADI",blank=True, null=True,max_length=100)
#     hour_s = models.PositiveSmallIntegerField(verbose_name="SAAT:",default=0,blank=True, null=True)  # Saati temsil etmek için
#     minute_s = models.PositiveSmallIntegerField(verbose_name="DAKİKA:",default=0,blank=True, null=True)  # Dakikayı temsil etmek için
#     TIMER_S_Exam_Date = models.DateTimeField(auto_now=True,verbose_name="SINAV SÜRESİ KAYIT TARİHİ")

#     def __str__(self):
#         return 'SINAV ADI={0},|SAAT={1}, |DAKİKA={2}'.format(
#         self.Exam_Name,
#         self.hour_s,
#         self.minute_s,
#         )
    
from django.core.exceptions import ValidationError

class TIMER_S(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="SINAV SÜRESİNİ YAZAN KİŞİ")
    Exam_Name = models.TextField(verbose_name="SINAV ADI", blank=True, null=True, max_length=100)
    hour_s = models.PositiveSmallIntegerField(verbose_name="SAAT:", default=0, blank=True, null=True)  # Saati temsil etmek için
    minute_s = models.PositiveSmallIntegerField(verbose_name="DAKİKA:", default=0, blank=True, null=True)  # Dakikayı temsil etmek için
    TIMER_S_Exam_Date = models.DateTimeField(auto_now=True, verbose_name="SINAV SÜRESİ KAYIT TARİHİ")

    def clean(self):
        if not 0 <= self.hour_s <= 24:
            raise ValidationError({'hour_s': 'Saat değeri 0 ile 24 arasında olmalıdır.'})
        if not 0 <= self.minute_s <= 60:
            raise ValidationError({'minute_s': 'Dakika değeri 0 ile 60 arasında olmalıdır.'})

    def __str__(self):
        return 'SINAV ADI={0},|SAAT={1}, |DAKİKA={2}'.format(
            self.Exam_Name,
            self.hour_s,
            self.minute_s,
        )
    
    class Meta:
        verbose_name_plural = "(TEKİL) SINAV SÜRESİ EKLEME"


#-------------------------------------------------------------------------------------------------------------------------------------------# 



#DENEME MODEL ALANI BAŞLANGIÇ


class TIMER_S_TESTTING(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="TEST SÜRESİNİ YAZAN KİŞİ")
    Testing_Name = models.TextField(verbose_name="TEST ADI", blank=True, null=True, max_length=100)
    hour_s = models.PositiveSmallIntegerField(verbose_name="SAAT:", default=0, blank=True, null=True)  # Saati temsil etmek için
    minute_s = models.PositiveSmallIntegerField(verbose_name="DAKİKA:", default=0, blank=True, null=True)  # Dakikayı temsil etmek için
    Testing_Name_Exam_Date = models.DateTimeField(auto_now=True, verbose_name="TEST SÜRESİ KAYIT TARİHİ")

    def clean(self):
        if not 0 <= self.hour_s <= 24:
            raise ValidationError({'hour_s': 'Saat değeri 0 ile 24 arasında olmalıdır.'})
        if not 0 <= self.minute_s <= 60:
            raise ValidationError({'minute_s': 'Dakika değeri 0 ile 60 arasında olmalıdır.'})

    def __str__(self):
        return 'SINAV ADI={0},|SAAT={1}, |DAKİKA={2}'.format(
            self.Testing_Name,
            self.hour_s,
            self.minute_s,
        )
    class Meta:
        verbose_name_plural = "(TEKİL) TEST SÜRESİ EKLEME"


class Testing_Result(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="CEVAP VEREN")
    Testing_Name = models.CharField(max_length=100, verbose_name="DENEME ADI", blank=True, null=True)
    Question_Id = models.IntegerField(verbose_name="SORU ID", blank=True, null=True)
    #Question_Id = models.CharField(max_length=110, verbose_name="SORU ID", blank=True, null=True)
    Question_Key = models.CharField(max_length=1, verbose_name="SORUNUN CEVAP ANAHTARI", blank=True, null=True)
    author_Key = models.CharField(max_length=1, verbose_name="CEVAP VERİLEN ŞIK", blank=False)
    True_Answer = models.CharField(max_length=1, default=2, verbose_name="CEVAP DOĞRU MU? ('0 => Yanlış, 1 => Doğru, 2 => Boş')", blank=True, null=True)

    def __str__(self):
        return 'DENEMEYE KATILAN={0}, DENEME ADI={1}, SORU ID={2}, CEVAP ANAHTARI={3}, SORUYA VERİLEN CEVAP={4}, SORUYU DOĞRU MU YAPTI?={5}'.format(
            self.author,
            self.Testing_Name,
            self.Question_Id,
            self.Question_Key,
            self.author_Key,
            self.True_Answer,
        )
    
    class Meta:
        verbose_name_plural = "(TEKİL) TEST SONUÇLARI"


class Testing_Table(models.Model):
    author=models.ForeignKey(User,on_delete = models.CASCADE,verbose_name="DENEMEMEYE KATILAN")# bunu django hazır kullanıcı tablosundan alıyoruz
    Testing_Name = models.CharField(max_length=100, verbose_name="DENEME ADI", blank=True, null=True)
    Total_Number_Of_Questions=models.CharField(max_length=3,verbose_name="TOPLAM SORU SAYISI", blank=True, null=True)
    Number_Of_True=models.CharField(max_length=3,verbose_name="TOPLAM DOĞRU SAYISI", blank=True, null=True)
    Number_Of_False=models.CharField(max_length=3,verbose_name="TOPLAM YANLIŞ SAYISI", blank=True, null=True)
    Number_Of_Empty=models.CharField(max_length=3,verbose_name="TOPLAM BOŞ SAYISI", blank=True, null=True)
    Testing_Score = models.CharField(max_length=3,verbose_name="DENEMEDEN ALDIĞI PUAN", blank=True, null=True)
    Testing_Rating = models.CharField(max_length=3,verbose_name="DENEME DERECESİ", blank=True, null=True)
    Completion_Time = models.CharField(max_length=50,verbose_name="DENEME BİTİRME SÜRESİ", blank=True, null=True)
    Testing_Date = models.DateTimeField(auto_now=False,verbose_name="DENEME BİTİRME TARİHİ")



    def __str__(self):
        return 'DENEME BİTİRME TARİHİ={0}'.format(
        self.Testing_Date
        )
    class Meta:
        verbose_name_plural = "(TEKİL) TEST SONUÇ TABLOSU"


class Testing_Choice(models.Model):
    Lessons_Name  = (
        ('Türk Dili ve Edebiyatı', 'Türk Dili ve Edebiyatı'),
        ('Matematik', 'Matematik'),
        ('Fizik', 'Fizik'),
        ('Kimya','Kimya'),
        ('Tarih','Tarih'),
        ('Biyoloji','Biyoloji'),
        ('Coğrafya','Coğrafya'),
        ('Din Kültürü ve Ahlak Bilgisi','Din Kültürü ve Ahlak Bilgisi')
    )

    Answer_Choice  = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D','D'),
        ('E','E')
    )
    Class_Choice  = (
        ('9. Sınıf', '9. Sınıf'),
        ('10. Sınıf', '10. Sınıf'),
        ('11. Sınıf', '11. Sınıf'),
        ('12. Sınıf','12. Sınıf')
    )

    author=models.ForeignKey(User,on_delete = models.CASCADE,verbose_name="SORUYU YAZAN")# bunu django hazır kullanıcı tablosundan alıyoruz
    Class_Choice=models.CharField(verbose_name="KAÇINCI SINIF SORUSU ?",choices=Class_Choice,null=True,blank=False,max_length=15)
    testi_cozen_kisi=models.ManyToManyField(User,default=None,related_name="testi_cozen_kisi",verbose_name="testi_cozen_kisi",blank=True, null=True,max_length=100)
    Lessons_Name = models.CharField(verbose_name="DERS ADI", choices=Lessons_Name, max_length=100, blank=False)
    Testing_Name=models.TextField(verbose_name="TEST ADI",blank=True, null=True,max_length=100)
    Question=models.TextField(verbose_name="SORU")
    Choice_A=models.TextField(verbose_name="A ŞIKKI",blank=True, null=True)
    Choice_B=models.TextField(verbose_name="B ŞIKKI",blank=True, null=True)
    Choice_C=models.TextField(verbose_name="C ŞIKKI",blank=True, null=True)
    Choice_D=models.TextField(verbose_name="D ŞIKKI",blank=True, null=True)
    Choice_E=models.TextField(verbose_name="E ŞIKKI",blank=True, null=True)
    # hour_s = models.PositiveSmallIntegerField(verbose_name="SAAT:",default=0,blank=True, null=True)  # Saati temsil etmek için
    # minute_s = models.PositiveSmallIntegerField(verbose_name="DAKİKA:",default=0,blank=True, null=True)  # Dakikayı temsil etmek için
    Answer_Choice=models.CharField(verbose_name="CEVAP", choices=Answer_Choice, max_length=1, blank=False)
    Question_Image=models.ImageField(upload_to='testing_and_exam_images/',blank=True, null=True, verbose_name="SORUYA FOTOĞRAF EKLEYİN")
    Created_Date=models.DateTimeField(auto_now=True,verbose_name="OLUŞTURMA TARİHİ")


    def __str__(self):
        #return f"{self.Lessons_Name},{self.Period_Name},{self.Exam_Name},{self.id}"
        return  'DENEMEYİ HAZIRLAYAN={0},TEST ADI={1}, SORU ID={2}, CEVAP ANAHTARI={3}'.format(
                    self.author, 
                    self.Testing_Name,
                    self.pk,
                    self.Answer_Choice,
                    )
    class Meta:
        verbose_name_plural = "(TEKİL) TEST SORU EKLEME"
#DENEME MODEL ALANI BİTİŞ
    
#-------------------------------------------------------------------------------------------------------------------------------------------# 

#TYT MODEL ALANI BAŞLANGIÇ
class TYT_Choice(models.Model):
    Lessons_Name  = (
        ('Matematik', 'Matematik'),
        ('Fizik', 'Fizik'),
        ('Kimya','Kimya'),
        ('Tarih','Tarih'),
        ('Biyoloji','Biyoloji'),
        ('Coğrafya','Coğrafya'),
        ('Türkçe','Türkçe'),
        ('Din Kültürü ve Ahlak Bilgisi','Din Kültürü ve Ahlak Bilgisi')
    )

    Answer_Choice  = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D','D'),
        ('E','E')
    )
    Date_Choice  = (
        ('2017','2017'),
        ('2018','2018'),
        ('2019','2019'),
        ('2020','2020'),
        ('2021','2021'),
        ('2022','2022'),
        ('2023','2023')

    )
    EXAM_Name  = (
        ('10 Haziran 2017', '10 Haziran 2017'),
        ('10 Haziran 2017', '23 Haziran 2018'),
        ('10 Haziran 2017', '15 Haziran 2019'),
        ('10 Haziran 2017', '27 Haziran 2020'),
        ('10 Haziran 2017', '26 Haziran 2021'),
        ('10 Haziran 2017', '18 Haziran 2022'),
        ('10 Haziran 2017', '17 Haziran 2023')
      )

    author=models.ForeignKey(User,on_delete = models.CASCADE,verbose_name="SORUYU YAZAN")# bunu django hazır kullanıcı tablosundan alıyoruz
    Date_Choice=models.CharField(verbose_name="HANGİ SENENİN SORUSU ?",choices=Date_Choice,null=True,blank=False,max_length=15)
    Lessons_Name = models.CharField(verbose_name="DERS ADI", choices=Lessons_Name, max_length=100, blank=False)
    EXAM_Name=models.TextField(verbose_name="SINAV ADI",choices=EXAM_Name,null=True,blank=False,max_length=100)
    tyt_cozen_kisi=models.ManyToManyField(User,default=None,related_name="tyt_cozen_kisi",verbose_name="tyt_cozen_kisi",blank=True, null=True,max_length=100)

    Question=models.TextField(verbose_name="SORU")
    Choice_A=models.TextField(verbose_name="A ŞIKKI",blank=True, null=True)
    Choice_B=models.TextField(verbose_name="B ŞIKKI",blank=True, null=True)
    Choice_C=models.TextField(verbose_name="C ŞIKKI",blank=True, null=True)
    Choice_D=models.TextField(verbose_name="D ŞIKKI",blank=True, null=True)
    Choice_E=models.TextField(verbose_name="E ŞIKKI",blank=True, null=True)
    # hour_s = models.PositiveSmallIntegerField(verbose_name="SAAT:",default=0,blank=True, null=True)  # Saati temsil etmek için
    # minute_s = models.PositiveSmallIntegerField(verbose_name="DAKİKA:",default=0,blank=True, null=True)  # Dakikayı temsil etmek için
    Answer_Choice=models.CharField(verbose_name="CEVAP", choices=Answer_Choice, max_length=1, blank=False)
    Question_Image=models.ImageField(upload_to='testing_and_exam_images/',blank=True, null=True, verbose_name="SORUYA FOTOĞRAF EKLEYİN")
    Created_Date=models.DateTimeField(auto_now=True,verbose_name="OLUŞTURMA TARİHİ")


    def __str__(self):
        #return f"{self.Lessons_Name},{self.Period_Name},{self.Exam_Name},{self.id}"
        return  'sınavı HAZIRLAYAN={0},SINAV ADI={1}, SORU ID={2}, CEVAP ANAHTARI={3}'.format(
                    self.author, 
                    self.EXAM_Name,
                    self.pk,
                    self.Answer_Choice,
                    )
    class Meta:
        verbose_name_plural = "TYT SORU EKLEME"


class TIMER_S_TYT(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="SINAV SÜRESİNİ YAZAN KİŞİ")
    Date_Choice = models.TextField(verbose_name="SINAV ADI", blank=True, null=True, max_length=100)
    hour_s = models.PositiveSmallIntegerField(verbose_name="SAAT:", default=0, blank=True, null=True)  # Saati temsil etmek için
    minute_s = models.PositiveSmallIntegerField(verbose_name="DAKİKA:", default=0, blank=True, null=True)  # Dakikayı temsil etmek için
    Testing_Name_Exam_Date = models.DateTimeField(auto_now=True, verbose_name="SINAV SÜRESİ KAYIT TARİHİ")

    def clean(self):
        if not 0 <= self.hour_s <= 24:
            raise ValidationError({'hour_s': 'Saat değeri 0 ile 24 arasında olmalıdır.'})
        if not 0 <= self.minute_s <= 60:
            raise ValidationError({'minute_s': 'Dakika değeri 0 ile 60 arasında olmalıdır.'})

    def __str__(self):
        return 'SINAV ADI={0},|SAAT={1}, |DAKİKA={2}'.format(
            self.Date_Choice,
            self.hour_s,
            self.minute_s,
        )

    class Meta:
        verbose_name_plural = "TYT SINAV SÜRESİ EKLEME"

class TYT_Table(models.Model):
    author=models.ForeignKey(User,on_delete = models.CASCADE,verbose_name="SINAVA KATILAN")# bunu django hazır kullanıcı tablosundan alıyoruz
    Date_Choice = models.CharField(max_length=100, verbose_name="SINAV ADI", blank=True, null=True)
    Total_Number_Of_Questions=models.CharField(max_length=3,verbose_name="TOPLAM SORU SAYISI", blank=True, null=True)
    Number_Of_True=models.CharField(max_length=3,verbose_name="TOPLAM DOĞRU SAYISI", blank=True, null=True)
    Number_Of_False=models.CharField(max_length=3,verbose_name="TOPLAM YANLIŞ SAYISI", blank=True, null=True)
    Number_Of_Empty=models.CharField(max_length=3,verbose_name="TOPLAM BOŞ SAYISI", blank=True, null=True)
    Exam_Score = models.CharField(max_length=3,verbose_name="SINAVDAN ALDIĞI PUAN", blank=True, null=True)
    Exam_Rating = models.CharField(max_length=3,verbose_name="SINAV DERECESİ", blank=True, null=True)
    Completion_Time = models.CharField(max_length=50,verbose_name="SINAV BİTİRME SÜRESİ", blank=True, null=True)
    Exam_Date = models.DateTimeField(auto_now=False,verbose_name="SINAV BİTİRME TARİHİ")



    def __str__(self):
        return 'SINAV BİTİRME TARİHİ={0}'.format(
        self.Date_Choice
        )
    
    class Meta:
        verbose_name_plural = "TYT SINAV TABLOSU"


class TYT_Result(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="CEVAP VEREN")
    Date_Choice = models.CharField(max_length=100, verbose_name="SINAV ADI", blank=True, null=True)
    Question_Id = models.IntegerField(verbose_name="SORU ID", blank=True, null=True)
    #Question_Id = models.CharField(max_length=110, verbose_name="SORU ID", blank=True, null=True)
    Question_Key = models.CharField(max_length=1, verbose_name="SORUNUN CEVAP ANAHTARI", blank=True, null=True)
    author_Key = models.CharField(max_length=1, verbose_name="CEVAP VERİLEN ŞIK", blank=False)
    True_Answer = models.CharField(max_length=1, default=2, verbose_name="CEVAP DOĞRU MU? ('0 => Yanlış, 1 => Doğru, 2 => Boş')", blank=True, null=True)

    def __str__(self):
        return 'SINAVA KATILAN={0}, SINAV ADI={1}, SORU ID={2}, CEVAP ANAHTARI={3}, SORUYA VERİLEN CEVAP={4}, SORUYU DOĞRU MU YAPTI?={5}'.format(
            self.author,
            self.Date_Choice,
            self.Question_Id,
            self.Question_Key,
            self.author_Key,
            self.True_Answer,
        )
    
    class Meta:
        verbose_name_plural = "TYT SINAV SONUÇLARI"
#-------------------------------------------------------------------------------------------------------------------------------------------# 
#TYT MODEL ALANI BİTİŞ
#-------------------------------------------------------------------------------------------------------------------------------------------# 
#AYT MODEL ALANI BAŞLANGIÇ
class AYT_Choice(models.Model):
    Lessons_Name  = (
        ('Matematik', 'Matematik'),
        ('Türk Dili ve Edebiyatı', 'Türk Dili ve Edebiyatı'),
        ('Fizik', 'Fizik'),
        ('Kimya','Kimya'),
        ('Tarih','Tarih'),
        ('Biyoloji','Biyoloji'),
        ('Coğrafya','Coğrafya'),
        ('Din Kültürü ve Ahlak Bilgisi','Din Kültürü ve Ahlak Bilgisi')
    )

    Answer_Choice  = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D','D'),
        ('E','E')
    )
    Date_Choice  = (
        ('2017','2017'),
        ('2018','2018'),
        ('2019','2019'),
        ('2020','2020'),
        ('2021','2021'),
        ('2022','2022'),
        ('2023','2023')

    )
    EXAM_Name  = (
        ('10 Haziran 2017', '10 Haziran 2017'),
        ('10 Haziran 2017', '23 Haziran 2018'),
        ('10 Haziran 2017', '15 Haziran 2019'),
        ('10 Haziran 2017', '27 Haziran 2020'),
        ('10 Haziran 2017', '26 Haziran 2021'),
        ('10 Haziran 2017', '18 Haziran 2022'),
        ('10 Haziran 2017', '17 Haziran 2023')
      )

    author=models.ForeignKey(User,on_delete = models.CASCADE,verbose_name="SORUYU YAZAN")# bunu django hazır kullanıcı tablosundan alıyoruz
    Date_Choice=models.CharField(verbose_name="HANGİ SENENİN SORUSU ?",choices=Date_Choice,null=True,blank=False,max_length=15)
    Lessons_Name = models.CharField(verbose_name="DERS ADI", choices=Lessons_Name, max_length=100, blank=False)
    ayt_cozen_kisi=models.ManyToManyField(User,default=None,related_name="ayt_cozen_kisi",verbose_name="ayt_cozen_kisi",blank=True, null=True,max_length=100)

    EXAM_Name=models.TextField(verbose_name="SINAV ADI",choices=EXAM_Name,null=True,blank=False,max_length=100)
    Question=models.TextField(verbose_name="SORU")
    Choice_A=models.TextField(verbose_name="A ŞIKKI",blank=True, null=True)
    Choice_B=models.TextField(verbose_name="B ŞIKKI",blank=True, null=True)
    Choice_C=models.TextField(verbose_name="C ŞIKKI",blank=True, null=True)
    Choice_D=models.TextField(verbose_name="D ŞIKKI",blank=True, null=True)
    Choice_E=models.TextField(verbose_name="E ŞIKKI",blank=True, null=True)
    # hour_s = models.PositiveSmallIntegerField(verbose_name="SAAT:",default=0,blank=True, null=True)  # Saati temsil etmek için
    # minute_s = models.PositiveSmallIntegerField(verbose_name="DAKİKA:",default=0,blank=True, null=True)  # Dakikayı temsil etmek için
    Answer_Choice=models.CharField(verbose_name="CEVAP", choices=Answer_Choice, max_length=1, blank=False)
    Question_Image=models.ImageField(upload_to='testing_and_exam_images/',blank=True, null=True, verbose_name="SORUYA FOTOĞRAF EKLEYİN")
    Created_Date=models.DateTimeField(auto_now=True,verbose_name="OLUŞTURMA TARİHİ")
    class Meta:
        verbose_name_plural = "AYT SORU EKLEME"


    def __str__(self):
        #return f"{self.Lessons_Name},{self.Period_Name},{self.Exam_Name},{self.id}"
        return  'sınavı HAZIRLAYAN={0},SINAV ADI={1}, SORU ID={2}, CEVAP ANAHTARI={3}'.format(
                    self.author, 
                    self.EXAM_Name,
                    self.pk,
                    self.Answer_Choice,
                    )

class AYT_TIMER_S(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="SINAV SÜRESİNİ YAZAN KİŞİ")
    Date_Choice = models.TextField(verbose_name="SINAV ADI", blank=True, null=True, max_length=100)
    hour_s = models.PositiveSmallIntegerField(verbose_name="SAAT:", default=0, blank=True, null=True)  # Saati temsil etmek için
    minute_s = models.PositiveSmallIntegerField(verbose_name="DAKİKA:", default=0, blank=True, null=True)  # Dakikayı temsil etmek için
    Testing_Name_Exam_Date = models.DateTimeField(auto_now=True, verbose_name="SINAV SÜRESİ KAYIT TARİHİ")

    def clean(self):
        if not 0 <= self.hour_s <= 24:
            raise ValidationError({'hour_s': 'Saat değeri 0 ile 24 arasında olmalıdır.'})
        if not 0 <= self.minute_s <= 60:
            raise ValidationError({'minute_s': 'Dakika değeri 0 ile 60 arasında olmalıdır.'})

    def __str__(self):
        return 'SINAV ADI={0},|SAAT={1}, |DAKİKA={2}'.format(
            self.Date_Choice,
            self.hour_s,
            self.minute_s,
        )
    class Meta:
        verbose_name_plural = "AYT SINAV SÜRESİ EKLEME"


class AYT_Table(models.Model):
    author=models.ForeignKey(User,on_delete = models.CASCADE,verbose_name="SINAVA KATILAN")# bunu django hazır kullanıcı tablosundan alıyoruz
    Date_Choice = models.CharField(max_length=100, verbose_name="SINAV ADI", blank=True, null=True)
    Total_Number_Of_Questions=models.CharField(max_length=3,verbose_name="TOPLAM SORU SAYISI", blank=True, null=True)
    Number_Of_True=models.CharField(max_length=3,verbose_name="TOPLAM DOĞRU SAYISI", blank=True, null=True)
    Number_Of_False=models.CharField(max_length=3,verbose_name="TOPLAM YANLIŞ SAYISI", blank=True, null=True)
    Number_Of_Empty=models.CharField(max_length=3,verbose_name="TOPLAM BOŞ SAYISI", blank=True, null=True)
    Exam_Score = models.CharField(max_length=3,verbose_name="SINAVDAN ALDIĞI PUAN", blank=True, null=True)
    Exam_Rating = models.CharField(max_length=3,verbose_name="SINAV DERECESİ", blank=True, null=True)
    Completion_Time = models.CharField(max_length=50,verbose_name="SINAV BİTİRME SÜRESİ", blank=True, null=True)
    Exam_Date = models.DateTimeField(auto_now=False,verbose_name="SINAV BİTİRME TARİHİ")



    def __str__(self):
        return 'SINAV BİTİRME TARİHİ={0}'.format(
        self.Date_Choice
        )
    class Meta:
        verbose_name_plural = "AYT SINAV TABLOSU"




class AYT_Result(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="CEVAP VEREN")
    Date_Choice = models.CharField(max_length=100, verbose_name="SINAV ADI", blank=True, null=True)
    Question_Id = models.IntegerField(verbose_name="SORU ID", blank=True, null=True)
    #Question_Id = models.CharField(max_length=110, verbose_name="SORU ID", blank=True, null=True)
    Question_Key = models.CharField(max_length=1, verbose_name="SORUNUN CEVAP ANAHTARI", blank=True, null=True)
    author_Key = models.CharField(max_length=1, verbose_name="CEVAP VERİLEN ŞIK", blank=False)
    True_Answer = models.CharField(max_length=1, default=2, verbose_name="CEVAP DOĞRU MU? ('0 => Yanlış, 1 => Doğru, 2 => Boş')", blank=True, null=True)

    def __str__(self):
        return 'SINAVA KATILAN={0}, SINAV ADI={1}, SORU ID={2}, CEVAP ANAHTARI={3}, SORUYA VERİLEN CEVAP={4}, SORUYU DOĞRU MU YAPTI?={5}'.format(
            self.author,
            self.Date_Choice,
            self.Question_Id,
            self.Question_Key,
            self.author_Key,
            self.True_Answer,
        )
    

    class Meta:
        verbose_name_plural = "AYT SINAV SONUÇLARI"



#////////////////////////USER_SUBSCRIBE_MODEL////////////////////////////////////////////////////////////////#

# class AuthorSubscription(models.Model):
#     author = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author_subscription', verbose_name="ÖĞRETMEN-KURUM")
#     subscribers = models.ManyToManyField(User, related_name='subscriptions', blank=True,verbose_name="ABONE OLUNAN KİŞİLER")
#     created_at = models.DateTimeField(auto_now_add=True,verbose_name="KAYIT TARİHİ")
#     updated_at = models.DateTimeField(auto_now=True,verbose_name="GÜNCELLEME TARİHİ")