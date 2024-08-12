from django.db import models


class tipoSeleccion(models.Model):

    descripcion = models.CharField(max_length=18)

    def __str__(self):
        return self.descripcion


class tipoTest(models.Model):

    descripcion = models.CharField(max_length=25)
    fechaCambio = models.DateField(auto_now_add=True)
    horaCambio = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.descripcion


class Test(models.Model):

    idTipoTest = models.ForeignKey(tipoTest, on_delete=models.CASCADE)
    idSeleccion = models.ForeignKey(tipoSeleccion, on_delete=models.CASCADE)
    nombreTest = models.TextField()
    abreviatura = models.CharField(max_length=10, null=True, blank=True)
    evalua = models.CharField(max_length=65)
    supervision = models.CharField(max_length=1)  # 'S' or 'N'
    duracion = models.PositiveSmallIntegerField()
    edadMin = models.PositiveSmallIntegerField(default=0)
    edadMax = models.PositiveSmallIntegerField(default=0)
    nroItems = models.PositiveSmallIntegerField()
    habilitado = models.CharField(max_length=1)  # 'S' or 'N'
    cuestionario = models.CharField(max_length=50, null=True, blank=True)
    respuesta = models.CharField(max_length=50, null=True, blank=True)
    fechaCambio = models.DateField(auto_now_add=True)
    horaCambio = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.nombreTest


class Alternativa(models.Model):

    idTest = models.ForeignKey(Test, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=20)
    puntuacion = models.PositiveSmallIntegerField()
    fechaCambio = models.DateField(auto_now_add=True)
    horaCambio = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.descripcion


class Dimension(models.Model):

    idTest = models.ForeignKey(Test, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=40)
    puntaje = models.PositiveSmallIntegerField()
    fechaCambio = models.DateField(auto_now_add=True)
    horaCambio = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.descripcion


class Escala(models.Model):

    idDimension = models.ForeignKey(Dimension, on_delete=models.CASCADE)
    inicioRango = models.PositiveSmallIntegerField()
    finRango = models.PositiveSmallIntegerField()
    resultado = models.CharField(max_length=20)
    tipo = models.CharField(max_length=10)
    fechaCambio = models.DateField(auto_now_add=True)
    horaCambio = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.resultado


class Capacidad(models.Model):

    idDimension = models.ForeignKey(Dimension, on_delete=models.CASCADE)
    nombreCapacidad = models.CharField(max_length=25)
    abreviatura = models.CharField(max_length=22)
    puntaje = models.PositiveSmallIntegerField()
    fechaCambio = models.DateField(auto_now_add=True)
    horaCambio = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.nombreCapacidad


class Pregunta(models.Model):

    idTest = models.ForeignKey(Test, on_delete=models.CASCADE)
    pregunta = models.TextField()
    fechaCambio = models.DateField(auto_now_add=True)
    horaCambio = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.pregunta


class Respuesta(models.Model):

    idPregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.CharField(max_length=10)
    puntuacion = models.PositiveSmallIntegerField()
    fechaCambio = models.DateField(auto_now_add=True)
    horaCambio = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.respuesta
