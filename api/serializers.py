from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from authentication.serializers import UserSerializer

from .constants import *

from .models import Question, Answer, Bookmark

from .mixins import (
    RepresentSerializerMixin,
    SetCreatorSerializerMixin,
    ShowBookmarkSerializerMixin,
)


class AnswerSerializer(
    ShowBookmarkSerializerMixin,
    serializers.ModelSerializer,
):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'


class AnswerCreateSerializer(
    RepresentSerializerMixin,
    SetCreatorSerializerMixin,
    ShowBookmarkSerializerMixin,
    serializers.ModelSerializer,
):
    question = serializers.IntegerField(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'
        representation_serializer = AnswerSerializer

    def to_internal_value(self, data):
        values = super().to_internal_value(data)
        values['created_by'] = self.context['user']
        values['question_id'] = self.context['kwargs']['question_id']
        return values


class QuestionSerializer(
    ShowBookmarkSerializerMixin,
    serializers.ModelSerializer,
):
    answers = AnswerSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class QuestionCreateSerializer(
    RepresentSerializerMixin,
    SetCreatorSerializerMixin,
    ShowBookmarkSerializerMixin,
    serializers.ModelSerializer,
):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        representation_serializer = QuestionSerializer


class BookmarkSerializer(serializers.ModelSerializer,):
    class Meta:
        model = Bookmark
        fields = '__all__'


class BookmarkCreateSerializer(
    RepresentSerializerMixin,
    SetCreatorSerializerMixin,
    serializers.ModelSerializer,
):
    created_by = UserSerializer(read_only=True)
    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(),
        required=False,
    )
    answer = serializers.PrimaryKeyRelatedField(
        queryset=Answer.objects.all(),
        required=False,
    )

    class Meta:
        model = Bookmark
        fields = '__all__'
        representation_serializer = BookmarkSerializer

    def validate(self, data):
        user = self.context.get('user')
        question = data.get('question')
        answer = data.get('answer')

        if (question and answer) or (not question and not answer):
            raise serializers.ValidationError(QUESTION_OR_ANSWER_REQUIRED)

        if question:
            if question.bookmarked(user):
                raise serializers.ValidationError(QUESTION_BOOKMARKED)
            if Bookmark.objects.filter(answer__in=question.answers.all(), created_by=user).exists():
                raise serializers.ValidationError(QUESTION_HAS_BOOKMARKED_ANSWER)

        if answer:
            if answer.bookmarked(user):
                raise serializers.ValidationError(ANSWER_BOOKMARKED)
            if answer.question.bookmarked(user):
                raise serializers.ValidationError(ANSWER_QUESTION_BOOKMARKED)

        return super().validate(data)
