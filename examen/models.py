from django.db import models

class Examen(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.CharField(max_length=50)
    horaInicioTest=models.DateTimeField()
    horaFinTest=models.DateTimeField()
    horaInicioPro=models.DateTimeField()
    horaFinPro=models.DateTimeField()
