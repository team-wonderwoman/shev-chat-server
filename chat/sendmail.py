# -*- coding: utf-8 -*-
import os
import getpass
import smtplib
import jwt, datetime,json
from django.conf import settings
from django.core import signing
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

# TODO 암호화과정, 메일 Verification

from email.message import EmailMessage
from email.mime.application import MIMEApplication
from common.const import const_value
from AuthSer.redis import redis_set

def create_verify_token(group_name,query):
    payload = {
        'group_name' : group_name,
        'user_email': query.user_email,
        'user_name': query.user_name,
        'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    verify_token = jwt.encode(payload, "SECRET_KEY", algorithm='HS256')

    print("verify_token")
    print(verify_token.decode('utf-8'))

    return verify_token


def decode_verify_token(encoded_verify_token):
    decoded_token = jwt.decode(encoded_verify_token, "SECRET_KEY", algorithms=['HS256'])

    print("decoded_verify_token 함수")
    print(decoded_token)

    return decoded_token['group_name']


# 그룹 초대 링크 이메일 보내는 함수
def send_verification_mail(group_name, participants, queryset):
    #password = getpass.getpass('Password : ')
    password = 'roqkfwk1234'
    print("password? : "+password)
    #print('request.data',end='')
    #print(request.data)
    # 그룹 이름
    #group_name = request.data['group_name']
    print("send_verification_mail_group_name : " + group_name)
    # 그룹 참여자의 이메일
    #participants = request.data['members']
    print("send_verification_mail_participants : ",end='')
    print(participants)

    message = EmailMessage()
    message['Subject'] = 'Verification Email : Participate in your group!'
    message['From'] = 'dpwlsl9504@naver.com'
    message['To'] = participants


    uid = str(urlsafe_base64_encode(force_bytes(queryset.id)),'utf-8')
    verify_token = str(urlsafe_base64_encode(force_bytes(create_verify_token(group_name,queryset))),'utf-8')

    print(uid)
    print(verify_token)

    link = """{}{}/{}/""".format(const_value['PARTICIPATION_LINK'],uid,verify_token)

    print("링크는?")
    print(link)

    contents = """Hello, We are Shev! You are invited to {}.\n
               If you want to participate {}, Please click the link below. {}\n               
               """.format(group_name,group_name,link)

    message.set_content(contents)

    #send_mail(message,contents)

    with smtplib.SMTP_SSL('smtp.naver.com',465) as server:
        server.ehlo()
        server.login('dpwlsl9504', password)
        server.send_message(message)

    print('Verification Email Send')

    # redis_set(verify_token, uid)




def send_registration_mail(self, serializer):
    password = 'roqkfwk1234'

    message = EmailMessage()
    message['Subject'] = 'Confirmation Email : Welcome to Shev!'
    message['From'] = 'dpwlsl9504@naver.com'
    message['To'] = self.serializer.data['user_email']

    link = const_value['CONFIRMATION_LINK']

    contents = """Hello, {}!\n We are Shev! Thanks to register in Shev.\n
               You are allowed to use our service right after click the link below. {}\n
               I hope you enjoy shev! Thank you.\n
               """.format(self.serializer.data['user_name'], const_value['CONFIRMATION_LINK'])

    message.set_content(contents)

    send_mail(message,password)

    # with smtplib.SMTP_SSL('smtp.naver.com', 465) as server:
    #     server.ehlo()
    #     server.login('cyj95428', password)
    #     server.send_message(message)

    print('Registration Email Send')


def send_mail(message, password):
    with smtplib.SMTP_SSL('smtp.naver.com', 465) as server:
        server.ehlo()
        server.login('dpwlsl9504', password)
        server.send_message(message)

    return