from django.urls import path

from home import views

urlpatterns = [
    path("banner/", views.BannerAPIView.as_view()),
    path('nav/',views.NavAPIView.as_view()),
]
