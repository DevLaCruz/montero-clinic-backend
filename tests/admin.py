# tests/admin.py
from django.contrib import admin
from .models import Test, Question, Answer, UserResponse


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1  # Número de respuestas iniciales que se mostrarán


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1  # Número de preguntas iniciales que se mostrarán
    inlines = [AnswerInline]


class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('name', 'description')
    search_fields = ('name',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'image')
    search_fields = ('text',)
    inlines = [AnswerInline]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    search_fields = ('text',)


admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserResponse)
