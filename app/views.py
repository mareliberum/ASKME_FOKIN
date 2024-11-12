from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import render, get_object_or_404
from .models import *






def paginate(objects_list, request, per_page=10):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)
    try:
        page = paginator.page(page_num)
    except InvalidPage:
        page = paginator.page(1)

    return page


def index(request):
    questions = Question.objects.new()
    page = paginate(questions, request)
    return render(request, 'index.html', context={'questions': page.object_list, 'page_obj': page})


def hot(request):
    hot_questions = Question.objects.best()
    page = paginate(hot_questions, request)

    return render(request, 'hot.html', context={'questions': page.object_list, 'page_obj': page})


def question(request, question_id):
    QUESTIONS = Question.objects.all()
    ANSWERS = Answer.objects.all()
    try:
        one_question = QUESTIONS[question_id - 1]
    except IndexError:
        return render(request, '404page.html')

    page = paginate(ANSWERS, request, 5)
    return render(request, 'question.html',
                  context={'question': one_question, 'answers': page.object_list, 'page_obj': page})


def tag(request, question_tag):
    # Найти тег по его имени
    tag = Tag.objects.filter(tag=question_tag).first()
    if tag is None:
        return render(request, '404page.html')
    # Получить связанные с этим тегом вопросы
    tagged_questions = tag.question.all()
    page = paginate(tagged_questions, request)
    return render(request, 'tag.html', context={'questions': page.object_list, 'page_obj': page, 'tag': question_tag})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')
