from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UsersViewSet,
    RegisterUserView,
    Verify_EmailAPIView,
    ChangePasswordView,
    LoginAPIView
)

router = DefaultRouter()
router.register('user', UsersViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('reg/', RegisterUserView.as_view(), name='register'),
    path('verify/<uuid:verify_code>', Verify_EmailAPIView.as_view(), name='verify_token'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('login/', LoginAPIView.as_view()),
]
