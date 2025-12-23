from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    created_at = models.DateTimeField(auto_created=True, verbose_name="Yaratilgan vaqti", auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True, verbose_name="Yangilangan vaqti", auto_now_add=True)
    
    class Meta:
        abstract = True

    
 
class Kurs(Base):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Student(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Ism", null=False, blank=False)
    last_name = models.CharField(max_length=50,null=False, blank=False, verbose_name="Familiya")
    exam = models.ForeignKey("Exam", on_delete=models.CASCADE, related_name="students")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Exam(Base):
    code = models.IntegerField(verbose_name="Imtihon kodi", unique=True, blank=True)
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE)
    guruh = models.ForeignKey("Guruh", on_delete=models.CASCADE)
    natija = models.ForeignKey(  "Natija", on_delete=models.CASCADE, blank=True, null=True)
    expired_at = models.DateTimeField(default=timezone.now()+timedelta(days=1), verbose_name="Imtihon tugash vaqti", blank=True)
    
    
class Natija(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    savol = models.ForeignKey("Savol", on_delete=models.CASCADE)
    javob = models.CharField(max_length=255) 
    def __str__(self):
        return str(self.score)
    
class Savol(models.Model):
    options = (
        ('variant_a', 'variant_a'),
        ('variant_b', 'variant_b'),
        ('variant_c', 'variant_c'),
        ('variant_d', 'variant_d'),
    )
    exam = models.ManyToManyField(Exam, verbose_name="Exam")
    matn = models.TextField(max_length=500, verbose_name="Savol matni")
    variant_a = models.CharField(max_length=255, verbose_name="Variant A")
    variant_b = models.CharField(max_length=255, verbose_name="Variant B")
    variant_c = models.CharField(max_length=255, verbose_name="Variant C")
    variant_d = models.CharField(max_length=255, verbose_name="Variant D")
    javob = models.CharField(choices=options)  
    
    def __str__(self):
        return self.matn
    
class Guruh(models.Model):
    telegram_id = models.CharField(max_length=500, verbose_name="Telegram ID", unique=True)
    name = models.CharField(max_length=100, verbose_name="Guruh nomi", unique=True)
    
    def __str__(self):
        return self.name