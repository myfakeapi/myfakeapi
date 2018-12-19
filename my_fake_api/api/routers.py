"""
Application API urlconfig
"""
from rest_framework import routers
from my_fake_api.api import views


router = routers.DefaultRouter()

router.register('logs', views.APIRequestViewSet, base_name="logs")
