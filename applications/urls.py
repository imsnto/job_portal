from django.urls import path, include

from applications.views import CreateApplication
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', CreateApplication, basename='applications')
urlpatterns = [
    path('', include(router.urls)),
]