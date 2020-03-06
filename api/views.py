from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from .serializers import (
    QuestionSerializer, QuestionCreateSerializer,
    AnswerSerializer, AnswerCreateSerializer,
    BookmarkSerializer, BookmarkCreateSerializer,
)
from .models import Question, Answer, Bookmark
from .mixins import (
    CustomViewSetMixin,
    WithoutUpdateGenericViewSet,
)


class QuestionViewSet(
    CustomViewSetMixin,
    viewsets.ModelViewSet,
):
    queryset = Question.objects.all()
    read_serializer_class = QuestionSerializer
    create_serializer_class = QuestionCreateSerializer


class AnswerViewSet(
    CustomViewSetMixin,
    viewsets.ModelViewSet,
):
    queryset = Answer.objects.all()
    read_serializer_class = AnswerSerializer
    create_serializer_class = AnswerCreateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        question_id = self.kwargs.get('question_id')
        return queryset.filter(question_id=question_id)


class BookmarkViewSet(
    CustomViewSetMixin,
    WithoutUpdateGenericViewSet,
):
    queryset = Bookmark.objects.all()
    read_serializer_class = BookmarkSerializer
    create_serializer_class = BookmarkCreateSerializer
