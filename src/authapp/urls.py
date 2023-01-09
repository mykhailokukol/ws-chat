from django.urls import path

from authapp import views


urlpatterns = [
    path('api/auth/users/', views.UserViewSet.as_view({
        'post': 'create',
        'get': 'list',
    })),
    path('api/auth/users/<int:pk>/', views.UserViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'patch': 'partial_update',
        'put': 'update',
    })),
    path('api/auth/token/', views.LoginUserApi.as_view({
        'post': 'post',
    })),
]
