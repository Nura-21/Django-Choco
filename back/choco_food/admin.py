from django.contrib import admin

from choco_food.models import Order, Restaurant, RestaurantCategory, ProductCategory, Product, Review

admin.site.register(Order)
admin.site.register(Restaurant)
admin.site.register(RestaurantCategory)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Review)
