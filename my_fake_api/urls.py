"""
Application url configuration
"""

from django.urls import path, include
from my_fake_api import handlers

from my_fake_api.api.routers import router

app_name = "my_fake_api"

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path("<uuid:api_id>/<path:path>", handlers.http_request_handler, name="http_handler"),
]
