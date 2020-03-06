from rest_framework import exceptions, mixins, viewsets, serializers

from authentication.serializers import UserSerializer


class CustomViewSetMixin():
    def get_permissions(self):
        if self.request.method != 'GET':
            return super().get_permissions()
        return []

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.read_serializer_class
        return self.create_serializer_class

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['kwargs'] = self.kwargs
        context['user'] = self.request.user
        return context

    def check_object_permissions(self, request, obj):
        if self.action in ['update', 'partial_update', 'destroy']:
            if request.user != obj.created_by:
                raise exceptions.NotAcceptable('Not allowed to perform this action')

        return super().check_object_permissions(request, obj)


class ShowBookmarkSerializerMixin():
    def to_representation(self, obj):
        values = super().to_representation(obj)
        user = self.context.get('user')

        if not user.is_anonymous:
            values['bookmarked'] = obj.bookmarked(user)

        return values


class RepresentSerializerMixin():
    def to_representation(self, obj):
        return self.Meta.representation_serializer(obj).data


class SetCreatorSerializerMixin():
    def to_internal_value(self, data):
        values = super().to_internal_value(data)
        values['created_by'] = self.context['user']
        return values


class WithoutUpdateGenericViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pass
