from django.db import models

# Create your models here.
class MyModel(models.Model):
    image = models.ImageField(upload_to='discover/',blank=True, null=True, verbose_name="KEŞFET İÇİN FOTOĞRAF EKLEYİN")
    _text= models.TextField(verbose_name="FOTOĞRAF METNİ EKLEYİN",blank=True, null=True)
    Created_Date=models.DateTimeField(auto_now=True,verbose_name="OLUŞTURMA TARİHİ")


    def __str__(self):
        #return f"{self.Lessons_Name},{self.Period_Name},{self.Exam_Name},{self.id}"
        return  'FOTOĞRAF METNİ={0},OLUŞTURMA TARİHİI={1}'.format(
                    self._text, 
                    self.Created_Date,

                    )