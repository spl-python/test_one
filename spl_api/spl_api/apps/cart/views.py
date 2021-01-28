from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from course.models import Course
from spl_api.settings.constants import IMG_SRC

class CartViewSet(ViewSet):
    # 登陆成功才可访问
    # permission_classes = [IsAuthenticated]

    def add_cart(self, request):
        course_id = request.data.get('course_id')
        print('course_id=', course_id)
        user_id = request.user.id
        print('user_id=', user_id)
        select = True  # 是否勾选
        expire = 0  # 有效期
        try:
            Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({'msg': '参数有误,课程不存在'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            redis_connection = get_redis_connection('cart')

            pipeline = redis_connection.pipeline()

            pipeline.multi()  # 开启管道

            pipeline.hset('cart_%s' % user_id, course_id, expire)  # 保存商品信息
            pipeline.sadd('selected_%s' % user_id, course_id)  # 保存商品的勾选状态
            # 执行
            pipeline.execute()

            cart_length = redis_connection.hlen('cart_%s' % user_id)
        except:
            return Response({'msg': '参数有误,购物车添加失败'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        return Response({'msg': '购物车添加成功', 'cart_length': cart_length}, status=status.HTTP_200_OK)

    def list_cart(self, request):
        user_id = request.user.id
        redis_connection = get_redis_connection('cart')
        cart_list_byte = redis_connection.hgetall('cart_%s' % user_id)
        select_list_byte = redis_connection.smembers('selected_%s' % user_id)
        print(user_id, redis_connection, cart_list_byte, select_list_byte)
        data = []
        for course_id_byte, expire_id_byte in cart_list_byte.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            try:
                course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            except Course.DoesNotExist:
                continue
            data.append({
                'selected': True if course_id_byte in select_list_byte else False,
                'course_img': IMG_SRC + course.course_img.url,
                'name': course.name,
                'id': course.id,
                'expire_id': expire_id,
                'price': course.price,
            })
        return Response(data)
