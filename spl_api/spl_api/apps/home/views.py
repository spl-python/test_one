from rest_framework.generics import ListAPIView

from home.models import Banner, Nav
from home.serializer import BannerModelSerializer, NavModelSerializer


class BannerAPIView(ListAPIView):
    """轮播图接口"""
    queryset = Banner.objects.filter(is_show=True, is_delete=False).order_by("-orders")
    serializer_class = BannerModelSerializer


class NavAPIView(ListAPIView):
    """头部导航栏"""

    queryset = Nav.objects.filter(is_show=True, is_delete=False).order_by("-orders")
    serializer_class = NavModelSerializer


# class FooterAPIView(ListAPIView):
#     """尾部导航栏"""
#     queryset = Nav.objects.filter(is_show=True, is_delete=False)
#     serializer_class = FootModelSerializer