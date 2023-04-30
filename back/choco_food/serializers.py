from rest_framework import serializers

from choco_food.models import Restaurant, Order, OrderProduct, Product, Review
from main.models import CreditCard


class RestaurantSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    img = serializers.URLField()
    delivery_time = serializers.IntegerField()
    delivery_price = serializers.IntegerField()
    rating = serializers.FloatField()


class RestaurantFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            'id',
            'title',
            'description',
            'address',
            'img',
            'delivery_time',
            'delivery_price',
            'category',
            'rating',
        )


class RestaurantCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    img = serializers.URLField()


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    img = serializers.URLField()
    category_id = serializers.IntegerField()


class ProductCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    icon = serializers.URLField()


class OrderProductSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product'
    )
    count = serializers.IntegerField()


class OrderListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    restaurant = serializers.CharField(source='restaurant.title')
    status = serializers.CharField()
    destination_address = serializers.CharField()
    products_cost = serializers.IntegerField()
    delivery_cost = serializers.IntegerField()
    total_cost = serializers.IntegerField()


class OrderFullSerializer(OrderListSerializer):
    products = serializers.SerializerMethodField()
    comment = serializers.CharField()

    def get_products(self, obj):
        return OrderProductSerializer(
            OrderProduct.objects.filter(
                order=obj
            ), many=True
        ).data


class OrderCreateSerializer(serializers.Serializer):
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        source='restaurant'
    )
    products = OrderProductSerializer(many=True)
    destination_address = serializers.CharField()
    comment = serializers.CharField(required=False)

    def create(self, validated_data):
        products = validated_data.pop('products')
        order = Order.objects.create(
            status=Order.PENDING,
            user=self.context['request'].user,
            **validated_data
        )
        for product in products:
            OrderProduct.objects.create(
                order=order,
                product=product['product'],
                count=product['count']
            )
        order.total_cost = order.products_cost + order.delivery_cost
        order.save()
        return order


class OrderPaySerializer(serializers.Serializer):
    credit_card_id = serializers.IntegerField()
    use_bonus_balance = serializers.BooleanField(required=False)

    def validate(self, attrs):
        credit_card_id = attrs.get('credit_card_id')
        if not CreditCard.objects.filter(
            owner=self.context['request'].user,
            id=credit_card_id
        ).exists():
            raise serializers.ValidationError('Такой кредитной карты не существует')
        return attrs

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if validated_data.get('use_bonus_balance'):
            if user.bonuses >= instance.total_cost:
                user.bonuses -= instance.total_cost
                instance.total_cost = 0
            else:
                instance.total_cost -= user.bonuses
                user.bonuses = 0
        else:
            user.bonuses += instance.products_cost * 0.1
        user.save()
        instance.status = Order.IN_PROGRESS
        instance.save()
        return instance


class OrderCancelSerializer(serializers.Serializer):
    comment = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        instance.status = Order.CANCELED
        instance.comment = validated_data.get('comment')
        instance.save()
        return instance


class ReviewSerializer(serializers.Serializer):
    class CreatorUserSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        phone = serializers.CharField()
        email = serializers.EmailField()

    comment = serializers.CharField()
    rate = serializers.IntegerField()
    creator = CreatorUserSerializer()


class ReviewCreateSerializer(serializers.Serializer):
    comment = serializers.CharField()
    rate = serializers.IntegerField()
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        source='restaurant'
    )

    def create(self, validated_data):
        return Review.objects.create(
            creator=self.context['request'].user,
            **validated_data
        )
