from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Citation
from .serializers import CitationSerializer


class AvailableDaysViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def days(self, request):
        days_with_availability = Citation.objects.filter(
            is_available=True).values('date').distinct()
        return Response(days_with_availability)


class AvailableTimesViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='available-times/(?P<date>\d{4}-\d{2}-\d{2})')
    def available_times(self, request, date=None):
        available_times = Citation.objects.filter(
            date=date, is_available=True).values('time')
        return Response(available_times)


class BookCitaViewSet(viewsets.ModelViewSet):
    queryset = Citation.objects.filter(is_available=True)
    serializer_class = Citation
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cita = serializer.save(user=self.request.user, is_available=False)
        # Aquí puedes enviar una confirmación de la reserva si es necesario.
