from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from choco_life.models import Event, EventCategory, Company, Certificate, UserCertificate

from choco_life.serializers import EventSerializer, EventCategorySerializer, CompanySerializer, \
    CertificateSerializer, UserCertificateSerializer, CertificateBuySerializer


class CompanyViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {}
    search_fields = ['title']

    def get_serializer_class(self):
        return CompanySerializer

    def get_queryset(self):
        return Company.objects.all()


class EventViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {
        'category_id': ['exact'],
    }
    search_fields = ['title']

    def get_serializer_class(self):
        return EventSerializer

    def get_queryset(self):
        return Event.objects.all()


class EventCategoryViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
):
    def get_serializer_class(self):
        return EventCategorySerializer

    def get_queryset(self):
        return EventCategory.objects.all()


class CertificateViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
):
    def get_serializer_class(self):
        return CertificateSerializer

    def get_queryset(self):
        return Certificate.objects.all()


class UserCertificateViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
):
    def get_serializer_class(self):
        if self.action == 'list':
            return UserCertificateSerializer
        if self.action == 'create':
            return CertificateBuySerializer

    def get_queryset(self):
        return UserCertificate.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_certificate = serializer.save()
        return Response(UserCertificateSerializer(user_certificate).data)
