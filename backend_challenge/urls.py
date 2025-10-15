from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from careers.views import CareerViewSet

router = DefaultRouter(trailing_slash=True)
router.register(r'careers', CareerViewSet, basename='career')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]