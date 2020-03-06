from django.db import models

from django.contrib.auth.models import User


class Question(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.title

    def bookmarked(self, user):
        if user.is_anonymous:
            return False

        return self.bookmarks.filter(created_by=user).exists()


class Answer(models.Model):
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')

    class Meta:
        unique_together = ['question', 'created_by']

    def __str__(self):
        return '%s - %s' % (self.question, self.content)

    def bookmarked(self, user):
        if user.is_anonymous:
            return False

        return self.bookmarks.filter(created_by=user).exists()


class Bookmark(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE, related_name='bookmarks')
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE, related_name='bookmarks')

    class Meta:
        unique_together = [
            ['created_by', 'question'],
            ['created_by', 'answer'],
        ]
