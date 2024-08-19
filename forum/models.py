from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FORUM(models.Model):
    topic_type  = (
        ('Genel', 'Genel'),
        ('Tartışma', 'Tartışma'),
        ('Soru-Cevap', 'Soru-Cevap'),

    )
    author=models.ForeignKey(User,on_delete = models.CASCADE,verbose_name="ENTRY YAZAN KİŞİ")
    text=models.TextField(verbose_name="Forum Metin",blank=True, null=True)
    topic_type=models.CharField(choices=topic_type,max_length=50,verbose_name="Konu Türü(Tipi)",null=True)
    number_of_answers=models.CharField(max_length=50,verbose_name="Cevap Sayısı",null=True,default="0")
    last_reply_date=models.CharField(max_length=50,verbose_name="Son Cevap Tarihi",default="0")
    created_date=models.DateTimeField(auto_now=True,verbose_name="Oluşturma Tarihi")
    forum_image=models.ImageField(upload_to='forum/',blank=True, null=True, verbose_name="Foruma Fotoğraf Ekleyin")



    def __str__(self):
        return  'Kullanıcı={0}, Konu={1},Metin{2}'.format(self.author, self.topic_type,self.text)
    

# class Forum_Comment(models.Model):
#     forum_text = models.ForeignKey(FORUM, on_delete=models.CASCADE, verbose_name="Yorum Yapılan Metin", related_name="forum_comments")  # FORUM modeline yapılan yorumlar
#     comment_author = models.ForeignKey("user.Profile", on_delete=models.CASCADE, verbose_name="YORUM YAPAN", related_name="comments")  # Yorum yapan kullanıcı
#     comment_content = models.TextField(blank=True, null=True, verbose_name="Yorum")
#     created_date = models.DateTimeField(auto_now=True, verbose_name="Oluşturma Tarihi")

#     def __str__(self):
#         return 'author={0}, content={1}'.format(self.comment_author, self.comment_content)



class Forum_Comment(models.Model):
    forum_text_id = models.IntegerField(verbose_name="Yorum Yapılan Metin ID")  # FORUM modeline yapılan yorumların ID'si
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="YORUM YAPAN", related_name="comments")  # Yorum yapan kullanıcı
    comment_content = models.TextField(blank=False, null=True, verbose_name="Yorum")
    created_date = models.DateTimeField(auto_now=True, verbose_name="Oluşturma Tarihi")

    def __str__(self):
        return 'author={0}, content={1}'.format(self.comment_author, self.comment_content)




class Forum_Like(models.Model):
    author = models.ForeignKey(User,on_delete = models.CASCADE,verbose_name="SORUYU BEĞENEN")
    forum = models.ForeignKey(FORUM,on_delete = models.CASCADE,verbose_name="BEĞENİ YAPILAN FORUM",related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('author', 'forum')
    def __str__(self):
         return  'KULLANICI={0}, SORU={1}'.format(self.author, self.forum)