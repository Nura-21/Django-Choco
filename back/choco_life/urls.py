from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('events', views.EventViewSet, basename='events')
router.register('event-categories', views.EventCategoryViewSet, basename='event_categories')
router.register('certificates', views.CertificateViewSet, basename='certificates')
router.register('companies', views.CompanyViewSet, basename='companies')
router.register('user-certificates', views.UserCertificateViewSet, basename='certificates_by_user')

urlpatterns = router.urls
