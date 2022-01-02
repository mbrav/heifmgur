from api.views import ImageViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'images', ImageViewSet, basename='images')

urlpatterns = [
    path('', include(router.urls)),
]
