# tests/serializers.py
from rest_framework import serializers
from .models import Test, Question, Answer, UserResponse


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, required=False)
    test_id = serializers.PrimaryKeyRelatedField(
        queryset=Test.objects.all(), source='test', write_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'image', 'answers', 'test_id']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers', [])
        question = Question.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)
        return question


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Test
        fields = ['id', 'name', 'description', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        test = Test.objects.create(**validated_data)
        for question_data in questions_data:
            answers_data = question_data.pop('answers', [])
            question = Question.objects.create(test=test, **question_data)
            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)
        return test


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ['id', 'user', 'question', 'selected_answer']
