
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

from .views import MistakeViewSet, SentenceViewSet

router = DefaultRouter()
router.register(r'mistakes', MistakeViewSet, basename='api-mistake')
router.register(r'sentences', SentenceViewSet, basename='api-sentence')
urlpatterns = router.urls