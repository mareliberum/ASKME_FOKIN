import copy

from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import render

QUESTIONS = [
    {
        'title': 'title ' + str(i),
        'id': i,
        'text': 'Text of the question' + str(i),
        'tag': 'tag' + str(i % 2)
    } for i in range(1, 30)
]
ANSWERS = [
    {
        'id': i,
        'text': 'Text of the answer ' + str(i),
    } for i in range(1, 30)

]


def paginate(objects_list, request, per_page=10):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)
    try:
        page = paginator.page(page_num)
    except InvalidPage:
        page = paginator.page(1)

    return page


def index(request):
    page = paginate(QUESTIONS, request)
    return render(request, 'index.html', context={'questions': page.object_list, 'page_obj': page})


def hot(request):
    hot_questions = copy.deepcopy(QUESTIONS)
    hot_questions.reverse()
    page = paginate(hot_questions, request)

    return render(request, 'hot.html', context={'questions': page.object_list, 'page_obj': page})


def question(request, question_id):
    one_question = QUESTIONS[question_id - 1]
    page = paginate(ANSWERS, request, 5)
    return render(request, 'question.html',
                  context={'question': one_question, 'answers': page.object_list, 'page_obj': page})


def tag(request, question_tag):
    tagged_questions = []

    for elem in QUESTIONS:
        if elem["tag"] == question_tag:
            tagged_questions.append(elem)

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
