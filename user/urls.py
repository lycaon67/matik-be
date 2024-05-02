from django.urls import path
from user import views


urlpatterns = [
    ## login
    path('login/', views.UserLogin.as_view()),
    ## register
    path('register/', views.UserRegister.as_view()),

    ##get, put, post
    path('users/', views.UserView.as_view()),

    path('admin/summary/', views.AdminView.as_view())

]