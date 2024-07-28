# tests/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestViewSet, QuestionViewSet, AnswerViewSet, UserResponseViewSet

router = DefaultRouter()
router.register(r'tests', TestViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'user_responses', UserResponseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
