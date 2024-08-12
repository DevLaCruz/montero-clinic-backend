from .models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response


class BaseModelViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        data = request.data

        # Check if the data is a list
        if isinstance(data, list):
            # Handle list of objects
            serializer = self.get_serializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            # Handle single object
            return super().create(request, *args, **kwargs)


class tipoSeleccionViewSet(BaseModelViewSet):
    queryset = tipoSeleccion.objects.all()
    serializer_class = tipoSeleccionSerializer


class tipoTestViewSet(BaseModelViewSet):
    queryset = tipoTest.objects.all()
    serializer_class = tipoTestSerializer


class TestViewSet(BaseModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class AlternativasViewSet(BaseModelViewSet):
    queryset = Alternativa.objects.all()
    serializer_class = AlternativasSerializer


class DimensionViewSet(BaseModelViewSet):
    queryset = Dimension.objects.all()
    serializer_class = DimensionSerializer


class EscalaViewSet(BaseModelViewSet):
    queryset = Escala.objects.all()
    serializer_class = EscalaSerializer


class CapacidadesViewSet(BaseModelViewSet):
    queryset = Capacidad.objects.all()
    serializer_class = CapacidadesSerializer


class PreguntasViewSet(BaseModelViewSet):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntasSerializer


class RespuestaViewSet(BaseModelViewSet):
    queryset = Respuesta.objects.all()
    serializer_class = RespuestaSerializer
