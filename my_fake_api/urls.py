"""
Application url configuration
"""

from django.urls import path, include
# from my_fake_api import views
from my_fake_api import handler

from my_fake_api.api_views import router

app_name = "my_fake_api"

urlpatterns = [
    # path("handlers/create/", views.HandlerCreate.as_view(), name="create_handler"),
    # path("handlers/<uuid:pk>/details", views.HandlerDetails.as_view(), name="handler_details"),
    # path("handlers/<uuid:pk>/logs", views.HandlerLogs.as_view(), name="handler_logs"),
    # path("handlers/", views.HandlerList.as_view(), name="handler_list"),

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path("<int:group_id>/<path:mocked_path>", handler.mocker_request_handler),
]
