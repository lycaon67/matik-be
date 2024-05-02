from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/<str:home_id>/', consumers.DeviceConsumer.as_asgi(), name="ws_home"),

]