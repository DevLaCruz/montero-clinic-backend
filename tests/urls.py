from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'tipo-seleccion', tipoSeleccionViewSet)
router.register(r'tipo-test', tipoTestViewSet)
router.register(r'tests', TestViewSet)
router.register(r'alternativas', AlternativasViewSet)
router.register(r'dimensiones', DimensionViewSet)
router.register(r'escalas', EscalaViewSet)
router.register(r'capacidades', CapacidadesViewSet)
router.register(r'preguntas', PreguntasViewSet)
router.register(r'respuestas', RespuestaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test/<int:test_id>/pregunta/<int:pregunta_id>/', PreguntasViewSet.as_view({'get': 'retrieve'})),
    # Add other custom URLs as needed
]
