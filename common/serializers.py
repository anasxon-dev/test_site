import random
from rest_framework import serializers
from .models import Exam, Kurs, Guruh, Natija, Student, Savol


class GuruhSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Guruh
        fields = ('id','telegram_id', 'name',)
        
class KursSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Kurs
        fields = ('id', 'name',)
        
class SavolSerializer(serializers.ModelSerializer):
    
    kurs = KursSerializer(many=True, read_only=True)
    
    class Meta:
        model = Savol
        fields = "__all__"
        
class StudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Student
        fields = ("id", 'first_name', "last_name", 'student',)
        
class NatijaSerializer(serializers.ModelSerializer):
    
    student = StudentSerializer()
    savol = SavolSerializer()
    
    class Meta:
        model = Natija
        fields = ("id", 'javob', "savol", 'student',)
    
        
class ExamSerializer(serializers.ModelSerializer):
    kurs = KursSerializer(read_only=True)
    guruh = GuruhSerializer(read_only=True)
    
    class Meta:
        model = Exam
        fields = ('code', 'kurs', 'guruh', 'expired_at',)
       
class ExamDetailSerializers(serializers.ModelSerializer):
    
    kurs = KursSerializer()
    guruh = GuruhSerializer()
    natija = NatijaSerializer(read_only=True)
    
    class Meta: 
        model = Exam
        fields = ("code", "kurs", "guruh", "natija")
    
class ExamCreateSerializer(serializers.ModelSerializer):
    kurs = serializers.PrimaryKeyRelatedField(
        queryset=Kurs.objects.all()
    )
    
    class Meta:
        model = Exam
        fields = ('code', 'kurs', 'guruh',  )
        
    def create(self, validated_data):
        validated_data['code'] = random.randint(1000, 9999)
        return super().create(validated_data)