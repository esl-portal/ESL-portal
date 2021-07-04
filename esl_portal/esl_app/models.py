from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Answer(models.Model):
    answer_text = models.CharField(max_length=30)
    related_question = models.ForeignKey("Question", on_delete=models.CASCADE, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    user_answers = models.ManyToManyField(User, through="UserAnswer")

    def __str__(self):
        return self.answer_text


class Question(models.Model):
    TYPES = (
        ("Single", "Single choice question"),
        ("Insert", "Question with insertion"),
        ("Multiple", "Multiple choice question")
    )
    question_text = models.CharField(max_length=500)
    type = models.CharField(max_length=8, choices=TYPES, default="Single")

    def __str__(self):
        return self.question_text


class Test(models.Model):
    LEVELS = (
        ("A1", "Elementary"),
        ("A2", "Pre-Intermediate"),
        ("B1", "Intermediate"),
        ("B2", "Upper-Intermediate"),
        ("C1", "Advanced"),
        ("C2", "Proficiency")
    )
    ASPECTS = (
        ("LX", "Lexis"),
        ("GR", "Grammar")
    )
    test_name = models.CharField(max_length=50)
    test_description = models.CharField(max_length=1000)
    test_short_description = models.CharField(max_length=200)
    level = models.CharField(max_length=2, choices=LEVELS)
    aspect = models.CharField(max_length=2, choices=ASPECTS)
    time_limit = models.PositiveSmallIntegerField()
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.test_name


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    answer_text = models.CharField(max_length=30)
    is_correct = models.BooleanField()


class Completion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    is_completed = models.BooleanField()
    taken_time = models.PositiveIntegerField()
    num_of_correct = models.PositiveSmallIntegerField()
    is_started = models.BooleanField()

    def __str__(self):
        return self.user.username.__str__() + "'s completion of " + self.test.__str__()


