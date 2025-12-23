from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, generics, status, mixins
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from .serializers import ExamCreateSerializer, KursSerializer, GuruhSerializer, ExamDetailSerializers
from .serializers import SavolSerializer
from common.models import Kurs,Guruh, Exam, Savol


class KursList(generics.ListCreateAPIView):
    queryset = Kurs.objects.all()
    serializer_class = KursSerializer
    permission_classes = [permissions.AllowAny]
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = KursSerializer(queryset, many=True)
        return Response(serializer.data)
    
class SavolList(generics.ListCreateAPIView):
    queryset = Savol.objects.all()
    serializer_class = SavolSerializer
    permission_classes = [permissions.AllowAny]
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = SavolSerializer(queryset, many=True)
        return Response(serializer.data)

class GuruhList(generics.ListCreateAPIView):
    queryset = Guruh.objects.all()
    serializer_class = GuruhSerializer
    permission_classes = [permissions.AllowAny]


class ExamCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=ExamCreateSerializer)
    
    def post(self, request):
        exam = ExamCreateSerializer(data=request.data)

        if exam.is_valid():
            exam.save()
            return Response(
                {"message": f"yaratildi {exam.data}"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            exam.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
class ExamView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, code):
        try:
            exam = Exam.objects.get(code = code)
            savol_obj = Savol.objects.filter(exam=exam)
            if exam.expired_at <= timezone.now():
                return Response(f"{code} - ushbu imtihon vaqti o'tgan", status=403)
            else:
                savollar = []
                for i in savol_obj:
                    savol = {
                        "matn": i.matn,
                        "variant_a": i.variant_a,
                        "variant_b": i.variant_b,
                        "variant_c": i.variant_c,
                        "variant_d": i.variant_d,
                        "javob": i.javob,
                    }
                    savollar.append(savol)

                if savollar:
                    return Response(
                        data={"savollar": savollar},
                        status=200
                    )

                return Response(
                    "Savollar yo'q",
                    status=404
                )
        except Exam.DoesNotExist:
            
            print(code)
            return Response(f"{code} - ushbu imtihon topilmadi", status=404)