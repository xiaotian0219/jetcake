from django.contrib.auth.models import AnonymousUser

from authentication.factories import UserFactory

from api.factories import QuestionFactory, AnswerFactory, BookmarkFactory

from .mixins import BaseTestCase


class QuestionModelTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.question = QuestionFactory()

    def test_str(self):
        self.assertEqual(str(self.question), self.question.title)

    def test_bookmarked(self):
        self.assertFalse(self.question.bookmarked(AnonymousUser()))
        self.assertFalse(self.question.bookmarked(self.primary_user))

        BookmarkFactory(created_by=self.primary_user, question=self.question)
        BookmarkFactory(created_by=self.secondary_user, question=self.question)

        self.assertTrue(self.question.bookmarked(self.primary_user))


class AnswerModelTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.answer = AnswerFactory()

    def test_str(self):
        self.assertEqual(str(self.answer), '%s - %s' % (self.answer.question, self.answer.content))

    def test_bookmarked(self):
        self.assertFalse(self.answer.bookmarked(AnonymousUser()))
        self.assertFalse(self.answer.bookmarked(self.primary_user))

        BookmarkFactory(created_by=self.primary_user, answer=self.answer)
        BookmarkFactory(created_by=self.secondary_user, answer=self.answer)

        self.assertTrue(self.answer.bookmarked(self.primary_user))
