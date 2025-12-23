from django.urls import path
from .views import ExamCreateView, KursList, GuruhList, ExamView, SavolList

urlpatterns = [
    path('create-exam/', ExamCreateView.as_view(), name='create-exam'),
    path('kurs-list/', KursList.as_view(), name='kurs-list'),
    path('guruh-list/', GuruhList.as_view(), name='guruh-list'),
    path('exam-start/<int:code>', ExamView.as_view(), name='ExamStart'),
    path('savol-list/', SavolList.as_view(), name='savol-list'),
]