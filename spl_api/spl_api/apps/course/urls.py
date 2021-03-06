from django.urls import path

from course import views

urlpatterns = [
    path("category/", views.CourseCategoryAPIView.as_view()),
    path("msg/", views.CourseAPIView.as_view()),
    path('detail/<str:pk>/',views.CourseDetialAPIView.as_view()),
    path('chapter/',views.CourseLessonAPIView.as_view())
]
