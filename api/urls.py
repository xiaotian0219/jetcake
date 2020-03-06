from django.urls import include, path

from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()

router.register(r'questions', QuestionViewSet)
router.register(r'questions/(?P<question_id>[^/.]+)/answers', AnswerViewSet)
router.register(r'bookmarks', BookmarkViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
]
