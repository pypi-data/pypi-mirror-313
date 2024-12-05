from django.urls import path
from rest_framework.routers import DefaultRouter

from .auth import LoginView, ForgotPasswordView, ResetPasswordView, UserOnboardView
from .views import PlatformUser, PlatformUserCustomField

router = DefaultRouter()
router.register(r"platform/users/custom-fields",PlatformUserCustomField,basename="platform.user.custom-fields")
router.register(r"platform/users", PlatformUser, basename="platform.user")

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<str:uidb64>/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),
    path('tenant-free-onboard/', UserOnboardView.as_view(), name='tenant-free-onboard'),
]

urlpatterns += router.urls
