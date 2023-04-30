from django.urls import path
from .views import LoginViewSet, MainUserViewSet, CreditCardViewSet

urlpatterns = [
    path('login/', LoginViewSet.as_view({
        'post': 'sign_in'
    })),
    path('', MainUserViewSet.as_view({
        'post': 'create',
        'put': 'update'
    })),
    path('<int:pk>/', MainUserViewSet.as_view({
        'get': 'retrieve'
    })),
    path('creditCards/', CreditCardViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('creditCards/<int:pk>', CreditCardViewSet.as_view({
        'put': 'update',
        'delete': 'destroy',
    }))
]
