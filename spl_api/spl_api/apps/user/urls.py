from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from user import views

urlpatterns = [
    path('login/',obtain_jwt_token),
    path('captcha/',views.CaptchaAPIView.as_view()),
    path('captchalogin/', views.CaptchaLoginAPIView.as_view()),

    path('register/',views.UserAPIView.as_view()),
    path("message/", views.MessageAPIView.as_view()),
]