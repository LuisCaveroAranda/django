from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('proceso/',views.iniciarProceso),
    path('resultado/',views.resultados)
]
