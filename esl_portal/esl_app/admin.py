from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

# Register your models here.

class TestQuestionAdmin(admin.ModelAdmin):
    fields = ['test', 'type', 'questions_for_test']

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Completion)
admin.site.register(UserAnswer)
admin.site.register(TestQuestion, TestQuestionAdmin)