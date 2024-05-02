from django.urls import path
from admin import views


urlpatterns = [
    ## Admin API
    # path('summary/', views.HomeAPI.as_view()),
    path('users/', views.UserListAPI.as_view()),
    path('users/<str:user_id>/', views.UserListAPI.as_view()),
    path('homes/', views.HomeListAPI.as_view()),
    path('homes/<str:home_id>/', views.HomeListAPI.as_view()),
    path('devices/', views.AdminDeviceAPI.as_view()),
    path('devices/<str:device_id>/', views.AdminDeviceAPI.as_view()),
]