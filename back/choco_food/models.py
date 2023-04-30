from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from django.db import models
from django.db.models import Sum, Avg

from main.models import MainUser


class RestaurantCategory(models.Model):
    title = models.CharField(max_length=50)
    img = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Restaurant(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    img = models.URLField(blank=True, null=True)
    delivery_time = models.PositiveIntegerField(blank=True, null=True)
    delivery_price = models.PositiveIntegerField(blank=True, null=True)
    category = models.ForeignKey(
        RestaurantCategory,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title

    @property
    def rating(self):
        return round(Review.objects.filter(restaurant=self).aggregate(rating=Avg('rate'))['rating'] or 5, 2)


class ProductCategory(models.Model):
    title = models.CharField(max_length=50)
    icon = models.URLField(blank=True, null=True)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='product_categories'
    )

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    img = models.URLField(blank=True, null=True)
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class Order(models.Model):
    PENDING = 'Pending'
    IN_PROGRESS = 'In progress'
    DELIVERED = 'Delivered'
    CANCELED = 'Canceled'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In progress'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.DO_NOTHING,
        related_name='orders'
    )
    user = models.ForeignKey(
        MainUser,
        on_delete=models.DO_NOTHING,
        related_name='orders',
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    destination_address = models.CharField(max_length=50)
    products = models.ManyToManyField(
        Product,
        through='OrderProduct'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    total_cost = models.PositiveIntegerField(blank=True, null=True)

    @property
    def products_cost(self):
        order_products = OrderProduct.objects.filter(order=self)
        total_price = 0
        for order_product in order_products:
            total_price += order_product.product.price * order_product.count
        return total_price

    @property
    def delivery_cost(self):
        order_product = OrderProduct.objects.filter(order=self)
        if not order_product.exists():
            return 0
        restaurant = order_product.first().product.restaurant
        base_delivery_price = restaurant.delivery_price
        return base_delivery_price * 1.5 if timezone.now().hour in range(12, 14) else base_delivery_price

    def __str__(self):
        return f'Order {self.id}'


class OrderProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    count = models.PositiveIntegerField()

    class Meta:
        unique_together = ('product', 'order')


class Review(models.Model):
    comment = models.TextField()
    rate = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    creator = models.ForeignKey(
        MainUser,
        on_delete=models.DO_NOTHING,
        related_name='reviews'
    )

    def __str__(self):
        return f'Review {self.id}'
