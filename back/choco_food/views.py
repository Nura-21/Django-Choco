from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from choco_food.models import Restaurant, RestaurantCategory, Order, Review
from choco_food.serializers import RestaurantSerializer, RestaurantFullSerializer, RestaurantCategorySerializer, \
    ProductSerializer, ProductCategorySerializer, OrderCreateSerializer, OrderFullSerializer, OrderPaySerializer, \
    OrderCancelSerializer, ReviewCreateSerializer, ReviewSerializer
from main.authentication import CustomAuthentication


class RestaurantViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin
):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {
        'category_id': ['exact'],
    }
    search_fields = ['title']

    def get_serializer_class(self):
        if self.action == 'list':
            return RestaurantSerializer
        if self.action == 'retrieve':
            return RestaurantFullSerializer
        if self.action == 'products':
            return ProductSerializer
        if self.action == 'product_categories':
            return ProductCategorySerializer

    def get_queryset(self):
        return Restaurant.objects.all()

    @action(methods=['GET'], detail=True)
    def products(self, request, pk, *args, **kwargs):
        restaurant = self.get_object()
        serializer = self.get_serializer(restaurant.product_set.all(), many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def product_categories(self, request, pk, *args, **kwargs):
        restaurant = self.get_object()
        serializer = self.get_serializer(restaurant.product_categories.all(), many=True)
        return Response(serializer.data)


class RestaurantCategoryViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin
):
    def get_serializer_class(self):
        return RestaurantCategorySerializer

    def get_queryset(self):
        return RestaurantCategory.objects.all()


class OrderViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.CreateModelMixin
):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderFullSerializer
        if self.action == 'create':
            return OrderCreateSerializer
        if self.action == 'pay':
            return OrderPaySerializer
        if self.action == 'cancel':
            return OrderCancelSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderFullSerializer(order).data)

    @action(methods=['PUT'], detail=True)
    def pay(self, request, pk, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderFullSerializer(order).data)

    @action(methods=['PUT'], detail=True)
    def cancel(self, request, pk, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderFullSerializer(order).data)


class ReviewViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.CreateModelMixin
):
    filter_backends = [DjangoFilterBackend]
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = {
        'restaurant_id': ['exact'],
    }

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        return Response(ReviewSerializer(review).data)
