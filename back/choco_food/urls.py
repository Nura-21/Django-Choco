from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('restaurants', views.RestaurantViewSet, basename='restaurants')
router.register('restaurant-categories', views.RestaurantCategoryViewSet, basename='restaurant_categories')
router.register('orders', views.OrderViewSet, basename='orders')
router.register('reviews', views.ReviewViewSet, basename='reviews')
urlpatterns = router.urls
