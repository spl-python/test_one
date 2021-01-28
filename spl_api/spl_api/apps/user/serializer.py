import re

from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_jwt.settings import api_settings

from user.models import UserInfo


class UserModelSerializer(ModelSerializer):
    token = serializers.CharField(max_length=1024, read_only=True, help_text='用户token')
    code = serializers.CharField(max_length=6, write_only=True, help_text='短信验证码')

    class Meta:
        model = UserInfo
        fields = ['phone', 'password', 'username', 'token', 'id', 'code']

        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'phone': {
                'write_only': True
            },
            'username': {
                'ready_only': True
            },
            'id': {
                'ready_only': True
            }
        }

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        code = attrs.get('code')

        if not re.match(r'^1[3-9]\d{9}$', phone):
            raise serializers.ValidationError('手机号格式错误')
        redis_connection = get_redis_connection('sms_code')
        phone_code = redis_connection.get('exp_%s' % phone)
        if phone_code.decode() != code:
            raise serializers.ValidationError('验证码输入错误')
        return attrs
        # TODO验证成功需要将验证码删除

    def create(self, validated_data):
        """重写保存对象的方法  完成用户信息的设置"""

        # 密码加密
        password = validated_data.get('password')
        hash_pwd = make_password(password)
        # 对用户进行设置默认值 手机号  随机字符串
        username = validated_data.get('phone')
        # 添加数据
        user_obj = UserInfo.objects.create(
            phone=username,
            username=username,
            password=hash_pwd
        )

        # 根据用户生成载荷
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # 根据载荷生成token
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user_obj)
        user_obj.token = jwt_encode_handler(payload)
        return user_obj

class CaptchaLoginModelSerializer(ModelSerializer):
    token = serializers.CharField(max_length=1024, read_only=True, help_text='用户token')
    code = serializers.CharField(max_length=6, write_only=True, help_text='短信验证码')

    class Meta:
        model = UserInfo
        fields = ['phone', 'password', 'username', 'token', 'id', 'code']

        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'phone': {
                'write_only': True
            },
            'username': {
                'ready_only': True
            },
            'id': {
                'ready_only': True
            }
        }

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        code = attrs.get('code')

        if not re.match(r'^1[3-9]\d{9}$', phone):
            raise serializers.ValidationError('手机号格式错误')
        redis_connection = get_redis_connection('sms_code')
        phone_code = redis_connection.get('exp_%s' % phone)
        if phone_code.decode() != code:
            raise serializers.ValidationError('验证码输入错误')
        return attrs
        # TODO验证成功需要将验证码删除