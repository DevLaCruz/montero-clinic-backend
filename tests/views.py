# tests/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Test, Question, Answer, UserResponse
from .serializers import TestSerializer, QuestionSerializer, AnswerSerializer, UserResponseSerializer
from math import ceil


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserResponseViewSet(viewsets.ModelViewSet):
    queryset = UserResponse.objects.all()
    serializer_class = UserResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='submit')
    def submit_responses(self, request):
        user = request.user
        test_id = request.data.get('test_id')
        responses = request.data.get('responses')

        if not test_id or not responses:
            return Response({'detail': 'test_id and responses are required.'}, status=status.HTTP_400_BAD_REQUEST)

        test = Test.objects.filter(id=test_id).first()
        if not test:
            return Response({'detail': 'Invalid test_id.'}, status=status.HTTP_400_BAD_REQUEST)

        for response in responses:
            question_id = response.get('question')
            selected_answer_id = response.get('selected_answer')

            question = Question.objects.filter(
                id=question_id, test=test).first()
            if not question:
                continue

            selected_answer = Answer.objects.filter(
                id=selected_answer_id, question=question).first()
            if not selected_answer:
                continue

            UserResponse.objects.create(
                user=user,
                question=question,
                selected_answer=selected_answer
            )

        # Calcular el puntaje final
        score = self.calculate_score(user, test)
        return Response({'status': 'responses submitted', 'score': score})

    def calculate_score(self, user, test):
        # Obtener todas las respuestas correctas del usuario para este test
        correct_responses = UserResponse.objects.filter(
            user=user,
            question__test=test,
            selected_answer__is_correct=True
        ).count()

        # Calcular el valor de cada pregunta
        total_questions = test.questions.count()
        if total_questions == 0:
            return 0

        high_note = 20
        score_per_question = high_note / total_questions

        # Redondear el puntaje si es impar
        total_score = correct_responses * score_per_question
        if total_questions % 2 != 0:
            total_score = ceil(total_score)

        return total_score
