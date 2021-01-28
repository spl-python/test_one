import requests

#发送验证码测试文件
class Message(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_message(self, phone, code):
        params = {
            'apikey': self.api_key,
            'mobile': phone,
            'text': '【毛信宇test】您的验证码是{code}。如非本人操作，请忽略本短信'.format(code=code)
        }

        request = requests.post(self.single_send_url, data=params)
        print(request)


if __name__ == '__main__':
    message = Message('40d6180426417bfc57d0744a362dc108')
    message.send_message('18739583760', '123456')
