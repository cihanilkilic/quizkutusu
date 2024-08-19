from django.db import models
from question.models import Lesson
from question.models import Classroom
from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class School(models.Model):
    school=models.CharField(verbose_name="Okul Adı",max_length=400)
    def __str__(self):
        return self.school
    class Meta:
        verbose_name_plural = "KULLANICIYA OKUL EKLEME"


class Profile(models.Model):
    USER_TYPE_CHOICES  = (
        ('Manager', 'Manager'),
        ('Assistant', 'Assistant'),
        ('Teacher', 'Teacher'),
        ('Student','Student'),
        ('Parents','Parents'),
        ('Publisher','Publisher'),
    )
    author=models.ForeignKey(User,on_delete = models.CASCADE,verbose_name="KULLANICI",related_name="profile")
    schools = models.ManyToManyField(School,verbose_name="Okul Adı", related_name="school_name",default=None)
    lessons = models.ManyToManyField(Lesson,null=True, blank=True, related_name="teacher_lessons")
    classrooms = models.ManyToManyField(Classroom,verbose_name="Kaçıncı Sınıf Öğretmeni?",related_name="classroom_name")
    avatars = models.ImageField(upload_to='user/', null=True,blank=False,default='user/default_user.jpg')
    biographys = models.CharField(max_length=150, null=True,blank=False)
    mobile_phone=models.CharField(unique=True,null=True, blank=False,max_length=11,verbose_name='Cep Telefonu')
    social_media_facebook=models.TextField(null=True, blank=True,verbose_name="Facebook Sosyal Medya")
    social_media_twitter=models.TextField(null=True, blank=True,verbose_name="Twitter Sosyal Medya")
    social_media_instagram=models.TextField(null=True, blank=True,verbose_name="İnstagram Sosyal Medya")
    social_media_tiktok=models.TextField(null=True, blank=True,verbose_name="Tiktok Sosyal Medya")
    user_types = models.CharField(default="Student", choices=USER_TYPE_CHOICES, max_length=20, blank=False)
    followers = models.ManyToManyField(User, verbose_name="Takipçi", related_name="follower_users", blank=True)
    following = models.ManyToManyField(User, verbose_name="Takip Etme", related_name="following_users", blank=True)

    created_date=models.DateTimeField(auto_now=True,verbose_name="Oluşturulma Tarihi")

    def __str__(self):
        return self.author.pk

    
    def __str__(self):
        return self.lessons

    def followers_count(self):
        return self.followers.count()
    
    def following_count(self):
        return self.following.count()


    def __str__(self):
        lessons_str = ", ".join(str(lesson) for lesson in self.lessons.all())
        return f"{self.author} - Lessons: {lessons_str}"


    class Meta:
        verbose_name_plural = "KULLANICI ÖZELLİKLERİ EKLEME"






#Model (USER SUBSCRIBE EDİT)

class UserSubscribeEdit(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_subscribe_edits')
    subscriber_one = models.IntegerField(verbose_name="Aylık Ödeme Planı", default=50, null=False, blank=False)
    subscriber_two = models.IntegerField(verbose_name="Üç Aylık Planı",default=140, null=False, blank=False)
    subscriber_three = models.IntegerField(verbose_name="6 Aylık Ödeme Planı",default=280, null=False, blank=False)
    subscriber_four = models.IntegerField(verbose_name="12 Aylık Ödeme Planı",default=580, null=False, blank=False)
    created_date=models.DateTimeField(auto_now=True,verbose_name="Oluşturulma Tarihi")

    def __str__(self):
        return f"{self.author.username} - Ödeme Planları"

    class Meta:
        verbose_name = "Kullanıcı Abonelik Düzenlemesi"
        verbose_name_plural = "Kullanıcı Abonelik Düzenlemeleri"
        ordering = ['author']










#Model (ABONE)


# class Abone(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='abonelikler')
#     abone_olunan_kullanicilar = models.ManyToManyField(User, related_name='aboneler')
#     start_date = models.DateTimeField(default=timezone.now)
#     end_date = models.DateTimeField()

#     def is_active(self):
#         return self.end_date > timezone.now()

#     def __str__(self):
#         return f"{self.user.username} - Abonelik"