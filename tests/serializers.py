from rest_framework import serializers
from .models import *

class tipoSeleccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = tipoSeleccion
        fields = '__all__'

class tipoTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = tipoTest
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class AlternativasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternativa
        fields = '__all__'

class DimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        fields = '__all__'

class EscalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escala
        fields = '__all__'

class CapacidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capacidad
        fields = '__all__'

class PreguntasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = '__all__'

class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = '__all__'
