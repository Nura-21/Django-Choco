from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import MainUser, CreditCard
from .serializers import MainUserSerializer, CreditCardSerializer, UserLoginSerializer, UserUpdateSerializer, \
    UserCreateSerializer

from .services import verify_user, create_token


class LoginViewSet(viewsets.GenericViewSet):
    def get_serializer_class(self):
        return UserLoginSerializer

    @action(methods=['POST'], detail=False)
    def sign_in(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        body = serializer.validated_data
        token = verify_user(request, body['email'], body['password'])
        return Response({'token': token})


class MainUserViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.UpdateModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.DestroyModelMixin
):
    def get_serializer_class(self):
        if self.action == 'update':
            return UserUpdateSerializer
        if self.action == 'create':
            return UserCreateSerializer
        return MainUserSerializer

    def get_queryset(self):
        return MainUser.objects.all()

    @action(methods=['PUT'], detail=False, permission_classes=[IsAuthenticated])
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CreditCardViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.UpdateModelMixin,
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.DestroyModelMixin
):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return CreditCardSerializer

    def get_queryset(self):
        return CreditCard.objects.filter(owner=self.request.user)
