import random

from django_redis import get_redis_connection
from rest_framework import status as http_status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from spl_api.libs.geetest import GeetestLib
from spl_api.settings import constants
from spl_api.utils.send_message import Message
from user.models import UserInfo
from user.serializer import UserModelSerializer, CaptchaLoginModelSerializer
from user.utils import get_user_by_account

pc_geetest_id = "45dbe199c830b4b9cb1bebd76fbbfdb7"
pc_geetest_key = "cbdff4cfb81c08cb1312f36b963fec22"


class CaptchaAPIView(APIView):
    user_id = 0
    status = False

    def get(self, request, *args, **kwargs):
        account = request.query_params.get('username')
        user = get_user_by_account(account)

        if user is None:
            return Response({'message': '用户不存在'}, status=http_status.HTTP_400_BAD_REQUEST)

        self.user_id = user.id

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)

        response_str = gt.get_response_str()
        return Response(response_str)

    def post(self, request, *args, **kwargs):
        """校验验证码"""

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.data.get("geetest_challenge", '')
        validate = request.data.get("geetest_validate", '')
        seccode = request.data.get("geetest_seccode", '')
        account = request.data.get('username')
        user = get_user_by_account(account)

        if user:
            # 验证结果是否正确
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status": "success"} if result else {"status": "fail"}
        return Response(result)

class UserAPIView(CaptchaAPIView):
    """用户注册"""
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer


class MessageAPIView(APIView):

    # 获取验证码 ,为手机号发送
    def get(self, request, *args, **kwargs):
        phone = request.query_params.get('phone')
        # 判断 手机号是否是 60s 内发送过短信的
        redis_connection = get_redis_connection('sms_code')
        mobile = redis_connection.get('sms_%s' % phone)

        if mobile is not None:
            return Response({
                'message': '您已经在60s内发送过短信了'},
                status=http_status.HTTP_400_BAD_REQUEST
            )

        # 为当前手机号随机生成验证码
        code = '%06d' % random.randint(0, 999999)

        # 将验证码保存到redis中
        redis_connection.setex('sms_%s' % phone, constants.SMS_EXPIRE_TIME, code)
        redis_connection.setex('sms_%s' % phone, constants.MOBILE_EXPIRE_TIME, code)

        try:
            message = Message(constants.API_KEY)
            message.send_message(phone, code)
            return Response({
                'message': '发送短信成功',
                'code': code
            }, status=http_status.HTTP_200_OK)
        except:
            return Response({
                'message': '短信发送失败,请稍后再试'
            }, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)

# 登陆短信验证码校验
class CaptchaLoginAPIView(ListAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = CaptchaLoginModelSerializer