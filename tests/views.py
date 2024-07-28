# tests/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User  # Importar el modelo User
from .models import Test, Question, Answer, UserResponse
from .serializers import TestSerializer, QuestionSerializer, AnswerSerializer, UserResponseSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class UserResponseViewSet(viewsets.ModelViewSet):
    queryset = UserResponse.objects.all()
    serializer_class = UserResponseSerializer

    @action(detail=False, methods=['post'])
    def submit_response(self, request):
        user = User.objects.get(id=request.data['user'])
        question = Question.objects.get(id=request.data['question'])
        selected_answer = Answer.objects.get(
            id=request.data['selected_answer'])
        response = UserResponse.objects.create(
            user=user, question=question, selected_answer=selected_answer)
        return Response({'status': 'response submitted'})
