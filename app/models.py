import random

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count


class QuestionManager(models.Manager):
    def best(self):
        """
        Возвращает "лучшие" вопросы, например, вопросы с наибольшим количеством лайков.
        Предполагается, что есть модель QuestionLike.
        """
        return self.annotate(like_count=Count('questionlike')).order_by('-like_count')

    def new(self):
        """
        Возвращает новые вопросы, отсортированные по дате создания.
        """
        return self.order_by('-created_at')


class TagManager(models.Manager):
    def get_popular_tags(self, count=10):
        tags = self.all()
        return random.sample(list(tags), min(len(tags), count))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=10000)
    # tag = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()

    def __str__(self):
        return self.title


class QuestionLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    unique_together = ["user", "question"]

    def __str__(self):
        return self.user.name


class Answer(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.CharField(max_length=10000)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name


class AnswerLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    unique_together = ["user", "answer"]

    def __str__(self):
        return self.user.name


class Tag(models.Model):
    tag = models.CharField(max_length=255)
    question = models.ManyToManyField(Question, related_name='tags')

    objects = TagManager()

    def __str__(self):
        return self.tag

