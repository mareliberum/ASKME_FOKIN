import random
import uuid
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike


class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio for data generation')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        # Создаем пользователей с уникальными именами
        users = [User(username=f'user_{uuid.uuid4().hex[:8]}') for _ in range(ratio)]
        User.objects.bulk_create(users)
        self.stdout.write(self.style.SUCCESS(f'{ratio} users created.'))


        # Создаем профили
        profiles = [Profile(user=user, name=f'User {i}') for i, user in enumerate(User.objects.all())]
        Profile.objects.bulk_create(profiles)
        self.stdout.write(self.style.SUCCESS(f'{len(profiles)} profiles created.'))

        # Создаем теги
        tags = [Tag(tag=f'Tag_{i}') for i in range(ratio)]
        Tag.objects.bulk_create(tags)
        tags = list(Tag.objects.all())
        self.stdout.write(self.style.SUCCESS(f'{len(tags)} tags created.'))

        # Создаем вопросы
        questions = []
        for i in range(ratio * 10):
            question = Question(
                user=random.choice(profiles),
                title=f'Question title {i}',
                text=f'This is the text for question {i}',
                # tag=random.choice(Tag.objects.all()).tag
            )
            questions.append(question)
        Question.objects.bulk_create(questions)
        self.stdout.write(self.style.SUCCESS(f'{len(questions)} questions created.'))
        questions = list(Question.objects.all())

        # Добавление связи тегов и вопросов
        for question in Question.objects.all():
            question.tags.add(*random.sample(tags, random.randint(1, min(3, len(tags)))))
        self.stdout.write(self.style.SUCCESS('Tags assigned to questions.'))

        # Создаем ответы
        answers = []
        for i in range(ratio * 100):
            answer = Answer(
                user=random.choice(profiles),
                text=f'This is the text for answer {i}',
                question=random.choice(questions)
            )
            answers.append(answer)
        Answer.objects.bulk_create(answers)
        self.stdout.write(self.style.SUCCESS(f'{len(answers)} answers created.'))

        # Обновляем ответы после bulk_create, чтобы получить доступ к ID
        answers = list(Answer.objects.all())

        # Создаем лайки на вопросы
        question_likes = []
        for i in range(ratio * 200):
            question_like = QuestionLike(
                user=random.choice(profiles),
                question=random.choice(questions)
            )
            question_likes.append(question_like)
        QuestionLike.objects.bulk_create(question_likes, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'{len(question_likes)} question likes created.'))

        # Создаем лайки на ответы
        answer_likes = []
        for i in range(ratio * 200):
            answer_like = AnswerLike(
                user=random.choice(profiles),
                answer=random.choice(answers)
            )
            answer_likes.append(answer_like)
        AnswerLike.objects.bulk_create(answer_likes, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'{len(answer_likes)} answer likes created.'))

        self.stdout.write(self.style.SUCCESS('Database has been filled with test data'))
