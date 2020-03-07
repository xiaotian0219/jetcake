import datetime
import factory

from authentication.factories import UserFactory

from api.models import Question, Answer, Bookmark


class QuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Question

    title = factory.Sequence(lambda n: 'Question %s' % n)
    content = factory.Sequence(lambda n: 'Question Content %s' % n)
    created_by = factory.SubFactory(UserFactory)


class AnswerFactory(factory.DjangoModelFactory):
    class Meta:
        model = Answer

    content = factory.Sequence(lambda n: 'Answer Content %s' % n)
    question = factory.SubFactory(QuestionFactory)
    created_by = factory.SubFactory(UserFactory)


class BookmarkFactory(factory.DjangoModelFactory):
    class Meta:
        model = Bookmark

    created_by = factory.SubFactory(UserFactory)
    question = factory.SubFactory(QuestionFactory)
    answer = factory.SubFactory(AnswerFactory)
