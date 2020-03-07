from django.contrib.auth.models import AnonymousUser

from rest_framework import status, exceptions

from authentication.factories import UserFactory

from api.constants import *
from api.factories import QuestionFactory, AnswerFactory, BookmarkFactory

from .mixins import BaseTestCase

from api.serializers import BookmarkSerializer
from api.models import Bookmark


class QuestionViewSetTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.count = 5

        for i in range(self.count):
            QuestionFactory(created_by=self.primary_user)

        for i in range(self.count):
            QuestionFactory(created_by=self.secondary_user)

    def test_create_question(self):
        create_data = {'title': 'Question title', 'content': 'Question content'}
        res = self.client.post('/api/questions/', create_data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['created_by']['id'], self.primary_user.id)

    def test_list_question(self):
        res = self.client.get('/api/questions/', format='json')
        self.assertEqual(len(res.data), self.count * 2)

    def test_get_question(self):
        res = self.client.get('/api/questions/1/', format='json')
        self.assertEqual(res.data['id'], 1)

    def test_update_question(self):
        update_data = {'title': 'Question update title', 'content': 'Question update content'}

        res = self.client.put('/api/questions/1/', update_data, format='json')
        self.assertEqual(res.data['title'], update_data['title'])

        res = self.client.put('/api/questions/6/', update_data, format='json')

        self.assertEqual(res.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(str(res.data['detail']), NOT_ALLOWED)

    def test_delete_question(self):
        res = self.client.delete('/api/questions/1/')

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        res = self.client.delete('/api/questions/6/')

        self.assertEqual(res.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(str(res.data['detail']), NOT_ALLOWED)


class AnswerViewSetTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.question1 = QuestionFactory(created_by=self.primary_user)
        self.question2 = QuestionFactory(created_by=self.primary_user)

        AnswerFactory(question=self.question1, created_by=self.primary_user)
        AnswerFactory(question=self.question1, created_by=self.secondary_user)

    def test_create_answer(self):
        create_data = {'content': 'Answer content'}

        res = self.client.post('/api/questions/2/answers/', create_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['content'], create_data['content'])

    def test_list_answer(self):
        res = self.client.get('/api/questions/1/answers/', format='json')
        self.assertEqual(len(res.data), 2)

    def test_get_answer(self):
        res = self.client.get('/api/questions/1/answers/1/', format='json')
        self.assertEqual(res.data['id'], 1)

    def test_update_answer(self):
        update_data = {'content': 'Updated answer content'}

        res = self.client.put('/api/questions/1/answers/1/', update_data, format='json')
        self.assertEqual(res.data['content'], update_data['content'])

        res = self.client.put('/api/questions/1/answers/2/', update_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_delete_answer(self):
        res = self.client.delete('/api/questions/1/answers/1/', format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        res = self.client.delete('/api/questions/1/answers/2/', format='json')
        self.assertEqual(res.status_code, status.HTTP_406_NOT_ACCEPTABLE)


class BookmarkViewSetTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.question1 = QuestionFactory(created_by=self.primary_user)
        self.answer1 = AnswerFactory(question=self.question1, created_by=self.secondary_user)

        self.question2 = QuestionFactory(created_by=self.secondary_user)
        self.answer2 = AnswerFactory(question=self.question2, created_by=self.primary_user)

        self.question3 = QuestionFactory(created_by=self.primary_user)

        BookmarkFactory(question=self.question1, answer=None, created_by=self.primary_user)
        BookmarkFactory(question=None, answer=self.answer2, created_by=self.primary_user)

        BookmarkFactory(question=self.question2, answer=None, created_by=self.secondary_user)
        BookmarkFactory(question=None, answer=self.answer1, created_by=self.secondary_user)

    def test_create_bookmark(self):
        create_data = {'question': 3}

        res = self.client.post('/api/bookmarks/', create_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['question'], create_data['question'])

        res = self.client.post('/api/bookmarks/', {}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['non_field_errors'][0], QUESTION_OR_ANSWER_REQUIRED)

        res = self.client.post('/api/bookmarks/', {'question': 1}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['non_field_errors'][0], QUESTION_BOOKMARKED)

        res = self.client.post('/api/bookmarks/', {'question': 2}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['non_field_errors'][0], QUESTION_HAS_BOOKMARKED_ANSWER)

        res = self.client.post('/api/bookmarks/', {'answer': 1}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['non_field_errors'][0], ANSWER_QUESTION_BOOKMARKED)

        res = self.client.post('/api/bookmarks/', {'answer': 2}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['non_field_errors'][0], ANSWER_BOOKMARKED)

    def test_list_bookmark(self):
        res = self.client.get('/api/bookmarks/', format='json')
        self.assertEqual(len(res.data), 4)

    def test_delete_bookmark(self):
        res = self.client.delete('/api/bookmarks/1/', format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        res = self.client.delete('/api/bookmarks/3/', format='json')
        self.assertEqual(res.status_code, status.HTTP_406_NOT_ACCEPTABLE)
