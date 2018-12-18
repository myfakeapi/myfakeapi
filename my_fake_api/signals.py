from django.dispatch import Signal


mocker_api_request = Signal(providing_args=["request"])
