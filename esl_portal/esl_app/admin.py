from django.contrib import admin
from .models import *


class AnswerInline(admin.StackedInline):
    extra = 4
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


# Register your models here.
admin.site.register(Test)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Completion)
admin.site.register(UserAnswer)
