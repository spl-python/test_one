from django.db.models import Q
from django.contrib.auth.backends import ModelBackend

from user.models import UserInfo


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'username': user.username,
        'user_id': user.id
    }


def get_user_by_account(account):
    try:
        user = UserInfo.objects.filter(Q(username=account) | Q(phone=account) | Q(email=account)).first()
    except UserInfo.DoesNotExist:
        return None
    else:
        return user

class UserAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        """根据账户获取用户对象"""

        user = get_user_by_account(username)
        #根据条件查询用户
        if user and user.check_password(password) and user.is_authenticated:
            return user
        else:
            return None