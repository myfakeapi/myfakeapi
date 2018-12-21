"""
Application API urlconfig
"""
from rest_framework import routers
from my_fake_api.api import views


router = routers.DefaultRouter()

router.register('apis', views.APIViewSet, base_name="apis")
router.register('handlers', views.APIHandlerViewSet, base_name="handlers")
router.register('logs', views.APIRequestViewSet, base_name="logs")
