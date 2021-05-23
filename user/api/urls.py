
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

from .views import CustomAuthToken, RegistrationToken

router = DefaultRouter()
urlpatterns = router.urls

urlpatterns += [path('login/', CustomAuthToken.as_view(), name='login'),
                path('register/', RegistrationToken.as_view(), name='register')]