# tests/models.py
from django.db import models
from django.contrib.auth.models import User


class Test(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.CharField(max_length=255)
    test = models.ForeignKey(
        Test, related_name='questions', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)  # Nuevo campo de imagen
    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        Question, related_name='answers', on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class UserResponse(models.Model):
    user = models.ForeignKey(
        User, related_name='responses', on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, related_name='user_responses', on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(
        Answer, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.question.text}'
