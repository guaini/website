from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json
import jwt
import time

from jwt import ExpiredSignatureError

from backend.models import User, Picture, Favorite, Tag, PictoTag


# Create your views here.
def index(request):
    return render(request, 'index.html')


def detail(request):
    return render(request, 'detail.html')


def to_login(request):
    return render(request, 'login.html')


def to_set(request):
    return render(request, 'set.html')


def to_star(request):
    return render(request, 'star.html')


def to_upload(request):
    return render(request, 'upload.html')


def adduser(request):
    info = request.content_params['data']
    name = info['username']
    if User.objects.filter(username=name).count():
        return JsonResponse({'ret': 1, 'msg': '用户名已存在'})
    user = User.objects.create(username=name,
                               password=make_password(info['passwd']),
                               email='hello@world.com',
                               birthday='2000',
                               sex='1',
                               country='none')
    return JsonResponse({'ret': 0, 'id': user.id})


def verify(request: HttpRequest):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is None:
        return 0
    try:
        info = jwt.decode(token, 'login', algorithms=['HS256'])
    except ExpiredSignatureError:
        return 0
    print(info)
    if info['is_Login']:
        return 1
    return 0


def signin(request: HttpRequest):
    username = request.content_params['username']
    password = request.content_params['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        exp_time = time.time() + 60 * 60 * 24
        token = jwt.encode({'username': username, 'is_Login': True, 'exp': exp_time}, 'login')
        str_token = str(token)
        return JsonResponse({'ret': 0, 'msg': '登录成功', 'token': str_token})
    else:
        return JsonResponse({'ret': 1, 'msg': '用户名或密码错误'})


def signout(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    info = jwt.decode(token, 'login', algorithms=['HS256'])
    username = info['username']
    token = jwt.encode({'username': username, 'is_Login': False}, 'login')
    str_token = str(token)
    return JsonResponse({'ret': 0, 'msg': '退出成功', 'token': str_token})


def update(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    info = jwt.decode(token, 'login', algorithms=['HS256'])
    nickname = info['username']
    new_info = request.content_params['newinfo']
    try:
        user = User.objects.get(username=nickname)
    except User.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': '用户不存在'})

    if 'nickname' in new_info:
        if User.objects.filter(username=new_info['nickname']).count():
            return JsonResponse({'ret': 1, 'msg': '用户名重复'})
        else:
            user.username = new_info['nickname']
            info['username'] = user.username

    if 'email' in new_info:
        user.email = new_info['email']
    if 'birthday' in new_info:
        user.birthday = new_info['birthday']
    if 'sex' in new_info:
        user.sex = new_info['sex']
    if 'country' in new_info:
        user.country = new_info['country']
    if 'wechat' in new_info:
        user.wechat = new_info['wechat']
    user.save()
    exp_time = time.time() + 60 * 60 * 24
    info['exp'] = exp_time
    token = jwt.encode(info, 'login')
    str_token = str(token)
    return JsonResponse({'ret': 0, 'msg': '更新成功', 'token': str_token})


def userInfo(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    decoded = jwt.decode(token, 'login', algorithms=['HS256'])
    username = decoded['username']
    user = User.objects.get(username=username)
    info = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'birthday': user.birthday,
        'sex': user.sex,
        'country': user.country,
        'wechat': user.wechat,
    }
    return JsonResponse({'ret': 0, 'userinfo': info})


def get_name_from_token(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    decoded = jwt.decode(token, 'login', algorithms=['HS256'])
    username = decoded['username']
    return username
