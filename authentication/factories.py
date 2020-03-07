import factory

from django.contrib.auth.models import User


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', 'email', 'first_name', 'last_name')

    username = factory.Sequence(lambda n: 'user-%s' % n)
    email = factory.Sequence(lambda n: 'user-%s@email.com' % n)
    first_name = factory.Sequence(lambda n: 'user-first-name-%s' % n)
    last_name = factory.Sequence(lambda n: 'user-last-name-%s' % n)

    @classmethod
    def password(cls):
        return 'password'

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        instance.set_password(cls.password())
        instance.save()
