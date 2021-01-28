from django.shortcuts import render
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView

from course.models import CourseCategory, Course, CourseChapter
from course.pagination import CoursePageNumberPagination
from course.serializer import CourseCategoryModelSerializer, CourseModelSerializer, CourseDetailModelSerializer, \
    CourseCapterModelSerializer


class CourseCategoryAPIView(ListAPIView):
    '''课程分类信息查询'''
    queryset = CourseCategory.objects.filter(is_show=True, is_delete=False).order_by("-orders")
    serializer_class = CourseCategoryModelSerializer


class CourseAPIView(ListAPIView):
    '''课程信息查询'''
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by('orders')
    serializer_class = CourseModelSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('course_category',)

    ordering_fields = ('id', 'student', 'price')

    pagination_class = CoursePageNumberPagination


class CourseDetialAPIView(RetrieveAPIView):
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by('orders')
    serializer_class = CourseDetailModelSerializer


class CourseLessonAPIView(ListAPIView):
    '''获取课程章节'''
    queryset = CourseChapter.objects.filter(is_show=True, is_delete=False).order_by('orders')
    serializer_class = CourseCapterModelSerializer

    filter_backends = [DjangoFilterBackend]
    filter_fields = ['course']
