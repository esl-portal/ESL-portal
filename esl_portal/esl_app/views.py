import doctest

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from .forms import *


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def main(request):
    context = {'is_authenticated': request.user.is_authenticated, 'request': request}
    return render(request, 'esl_app/main.html', context)


def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            if request.user.is_superuser:
                return redirect('/admin')
            else:
                return redirect('/main')
        else:
            form = UserLoginForm()
            return render(request, 'esl_app/login.html', {'wrong_credentials': True,
                                                          'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('/main/')
        else:
            form = UserLoginForm()
            return render(request, 'esl_app/login.html', {'wrong_credentials': False,
                                                          'form': form})


def login_forgot(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        form = UserForgotForm(request.POST)
        if User.objects.filter(username=username).count() != 0:
            user = User.objects.get(username=username)
            if form.is_valid():
                user.set_password(password)
                user.save()
                return redirect(to='/login/')
            else:
                return render(request, 'esl_app/forgot.html', {'form': form})
        else:
            form = UserForgotForm(request.POST)
            return render(request, 'esl_app/forgot.html', {'wrong_credentials': True,
                                                           'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('/main/')
        else:
            form = UserForgotForm()
            return render(request, 'esl_app/forgot.html', {'wrong_credentials': False,
                                                           'form': form})


def log_out(request):
    logout(request)
    return redirect('/main/')


def register(request):
    if request.user.is_authenticated:
        return redirect('/main/')
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid() and user_form.unique():
            new_user = User.objects.create_user(username=request.POST['username'],
                            first_name=request.POST['first_name'],
                            email=request.POST['email'],
                            password=request.POST['password'])
            return redirect('/login/')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'esl_app/register.html', {'user_form': user_form})


@login_required(login_url='/login/')
def profile_completed(request):
    user = request.user
    completions = Completion.objects.filter(user=user, is_completed=True)
    is_empty = len(completions) == 0
    is_authenticated = request.user.is_authenticated
    return render(request, 'esl_app/completed.html', {'completions': completions,
                                                      'is_empty': is_empty,
                                                      'is_authenticated': is_authenticated})


@login_required(login_url='/login/')
def profile_options(request):
    user = request.user
    if request.method == 'POST':
        form = UserChangeData(request.POST)
        if form.is_valid():
            new_username = request.POST['new_username']
            new_email = request.POST['new_email']
            new_first_name = request.POST['new_first_name']
            if user.username != new_username and new_username != '' and new_username is not None:
                user.username = new_username
            if user.email != new_email and new_email != '' and new_email is not None:
                user.email = new_email
            if user.first_name != new_first_name and new_first_name != '' and new_first_name is not None:
                user.first_name = new_first_name
            if request.POST['new_password'] != '':
                user.set_password(request.POST['new_password'])
            user.save()
            everything_empty = new_username == '' and new_email == '' and new_first_name == '' and request.POST['new_password'] == ''
            return render(request, 'esl_app/options.html', {'user': request.user, 'form': form, 'everything_empty': everything_empty})
    else:
        data = {'new_username': user.username,
                'new_first_name': user.first_name,
                'new_email': user.email}
        form = UserChangeData(initial=data)
    return render(request, 'esl_app/options.html', {'user': request.user,
                                                    'form': form})


def test_list(request):
    list_of_tests = None
    finished = request.GET.get('finished')
    is_authenticated = request.user.is_authenticated
    if finished is None:
        list_of_tests = get_list_or_404(Test.objects.all())
    else:
        int_finished = int(finished)
        finished = int_finished
        if int_finished == 1:
            if request.user.is_anonymous:
                list_of_tests = []
            else:
                list_of_tests = Test.objects.filter(completion__user=request.user, completion__is_completed=True)
        else:
            list_of_tests = Test.objects.exclude(completion__is_completed=True)
    return render(request, 'esl_app/tests.html', {'list': list_of_tests, 'is_authenticated': is_authenticated, 'finished_param': finished})


@login_required(login_url='/login/')
def test(request, test_id):
    some_test = get_object_or_404(Test, pk=test_id)
    completion = Completion.objects.filter(test_id=test_id, user__username=request.user.username)
    is_started = None
    is_completed = None
    if completion.count() > 0:
        completion = completion.first()
        is_started = completion.is_started
        is_completed = completion.is_completed
    else:
        is_started = False
        is_completed = False
    return render(request, 'esl_app/some_test.html', {'some_test': some_test, 'is_started': is_started, 'is_completed': is_completed})


@login_required(login_url='/login/')
def test_result(request, test_id):
    completion = Completion.objects.get(user__username=request.user.username, test_id=test_id)
    user_answers = list(UserAnswer.objects.filter(user__username=request.user.username,
                                                  answer__related_question__test=Test.objects.get(pk=test_id)))
    correct_answers_set = list(Answer.objects.filter(is_correct=True, related_question__test=Test.objects.get(pk=test_id)))
    correct_answers = {}
    for correct_answer in correct_answers_set:
        correct_answers[correct_answer.related_question.question_text] = correct_answer.answer_text
    return render(request, 'esl_app/result.html', {'completion': completion,
                                                   'amount_of_questions':
                                                       Test.objects.get(pk=test_id).questions.count(),
                                                   'user_answers': user_answers,
                                                   'correct_answers': correct_answers})


@login_required(login_url='/login/')
def profile(request):
    return render(request, 'esl_app/profile.html', {'user': request.user})


def start_test(request, test_id):
    completions = Completion.objects.filter(test_id=test_id, user__username=request.user.username)
    count = None
    question = None
    is_last = None
    user_answers = UserAnswer.objects.filter(user=request.user, answer__related_question__test=Test.objects.get(pk=test_id))
    if completions.count() > 0:
        first_completion = completions.first()
        if first_completion.is_completed or user_answers.count() == 0:
            user_answers.delete()
            count = 1
            first_completion.is_completed = False
            first_completion.number_of_last_answered_question = 0
            first_completion.num_of_correct = 0
            first_completion.save()
            question = Test.objects.get(pk=test_id).questions.order_by('id')[0]
            is_last = False
        else:
            count = first_completion.number_of_last_answered_question + 1
            question = Test.objects.get(pk=test_id).questions.order_by('id')[count - 1]
            # first_completion.number_of_last_answered_question += 1
            # first_completion.save()
            is_last = True if Test.objects.get(pk=test_id).questions.count() == count else False
    else:
        count = 1
        completion = Completion(user=request.user, test_id=test_id, is_completed=False, is_started=True,
                                number_of_last_answered_question=0, num_of_correct=0)
        completion.save()
        question = Test.objects.get(pk=test_id).questions.order_by('id')[0]
        is_last = False

    answers = list(Answer.objects.filter(related_question=question).values_list('answer_text'))
    response = {'num_of_question': count, 'question_text': question.question_text, 'type_of_question': question.type,
                'answers': answers, 'num_of_answers': len(answers), 'is_last': is_last}
    return JsonResponse(response)


def next_question(request, test_id):
    count = int(request.GET['count']) + 1
    question = Test.objects.get(pk=test_id).questions.order_by('id')[int(request.GET['count'])]
    answers = list(Answer.objects.filter(related_question=question).values_list('answer_text'))
    is_last = True if Test.objects.get(pk=test_id).questions.count() == count else False
    response = {'num_of_question': count, 'question_text': question.question_text, 'type_of_question': question.type,
                'answers': answers, 'num_of_answers': len(answers), 'is_last': is_last}
    return JsonResponse(response)


def previous_question(request, test_id):
    count = int(request.GET['count']) - 1
    question = Test.objects.get(pk=test_id).questions.order_by('id')[int(request.GET['count']) - 2]
    answers = list(Answer.objects.filter(related_question=question).values_list('answer_text'))
    is_last = True if Test.objects.get(pk=test_id).questions.count() == count else False
    response = {'num_of_question': count, 'question_text': question.question_text, 'type_of_question': question.type,
                'answers': answers, 'num_of_answers': len(answers), 'is_last': is_last}
    return JsonResponse(response)


def respond(request, test_id):
    if is_ajax(request):
        count = int(request.POST['count'])
        is_last = request.POST['is_last']
        if is_last == 'false':
            is_last = False
        else:
            is_last = True
        completion = Completion.objects.get(user__username=request.user.username, test=Test.objects.get(pk=test_id))
        test_question_answer = list(
            Answer.objects.filter(related_question=Question.objects.get(question_text=request.POST['question_text']),
                                  related_question__test=Test.objects.get(pk=test_id), is_correct=True).values_list(
                'answer_text', flat=True))
        user_answer = str(request.POST['answer']).split("|")
        if user_answer[-1] == '' and len(user_answer) > 1:
            user_answer.__delitem__(-1)
        is_correct = True
        for answer in user_answer:
            if not test_question_answer.__contains__(answer):
                is_correct = False
                break
        if len(user_answer) != len(test_question_answer):
            is_correct = False
        print(is_correct)
        if (len(UserAnswer.objects.filter(user__username=request.user.username,
                                          answer__related_question=Question.objects.get(
                                              question_text=request.POST['question_text']),
                                          answer__related_question__test=Test.objects.get(pk=test_id))) != 0):
            stored_user_answer = UserAnswer.objects.filter(user=request.user,
                                                           answer__related_question=Question.objects.get(
                                                               question_text=request.POST['question_text']),
                                                           answer__related_question__test=Test.objects.get(pk=test_id))
            if list(stored_user_answer.values_list('is_correct', flat=True)).__contains__(False) and is_correct == True:
                completion.num_of_correct += 1
                completion.number_of_last_answered_question = count
                completion.save()
            elif not list(stored_user_answer.values_list('is_correct', flat=True)).__contains__(False) \
                    and len(list(stored_user_answer.values_list('is_correct', flat=True))) == len(test_question_answer) \
                    and is_correct == False:
                completion.num_of_correct -= 1
                completion.number_of_last_answered_question = count
                completion.save()
            elif len(list(stored_user_answer.values_list('is_correct', flat=True))) != len(test_question_answer) \
                    and is_correct == True:
                completion.num_of_correct += 1
                completion.number_of_last_answered_question = count
                completion.save()
            stored_user_answer.update(is_correct=is_correct)
        else:
            for answer in user_answer:
                if list(Answer.objects.filter(answer_text=answer,
                                              related_question=Question.objects.get(
                                                  question_text=request.POST['question_text']),
                                              related_question__test=Test.objects.get(pk=test_id)).values_list(
                    'answer_text', flat=True)).__contains__(answer):

                    stored_answer = Answer.objects.get(answer_text=answer,
                                                       related_question=Question.objects.get(
                                                           question_text=request.POST['question_text']),
                                                       related_question__test=Test.objects.get(pk=test_id))
                else:
                    stored_answer = Answer.objects.get(
                        related_question=Question.objects.get(question_text=request.POST['question_text']),
                        related_question__test=Test.objects.get(pk=test_id), is_correct=True)

                stored_is_correct = True if test_question_answer.__contains__(answer) else False
                stored_user_answer = UserAnswer(user=request.user, answer=stored_answer,
                                                is_correct=stored_is_correct,
                                                answer_text=answer)
                stored_user_answer.save()

            if is_correct:
                completion.num_of_correct += 1
            completion.number_of_last_answered_question = count
            completion.save()
        print(is_last)
        return JsonResponse({'is_correct': is_correct, 'is_last': is_last, 'num_of_question': count})


def finish_test(request, test_id):
    completion = Completion.objects.get(user__username=request.user.username, test_id=test_id)
    completion.is_completed = True
    completion.save()
    response = {'redirect_url': 'result/'}
    return JsonResponse(response)


def about(request):
    is_authenticated = request.user.is_authenticated
    return render(request, 'esl_app/about.html', {'is_authenticated': is_authenticated})


def contacts(request):
    is_authenticated = request.user.is_authenticated
    return render(request, 'esl_app/contacts.html', {'is_authenticated': is_authenticated})


def error_404(request, exception=None):
    is_authenticated = request.user.is_authenticated
    return render(request, 'esl_app/404.html', {'is_authenticated': is_authenticated})
