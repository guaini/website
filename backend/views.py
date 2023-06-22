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


def upload(request: HttpRequest):
    data = request.POST.dict()['data']
    data = json.loads(data)
    size = data['size']
    tags = data['tags']
    name = data['name']
    picture = request.FILES.get('file')
    print(data, picture)
    token = request.META.get('HTTP_AUTHORIZATION')
    decoded = jwt.decode(token, 'login', algorithms=['HS256'])
    username = decoded['username']
    uploader = User.objects.get(username=username)
    result = Picture.objects.create(img=picture,
                                    imgname=name,
                                    size=size,
                                    uploader=uploader,
                                    num_like=0,
                                    num_star=0,
                                    num_view=0)
    for tag_name in tags:
        try:
            tag = Tag.objects.get(tname=tag_name)
        except Tag.DoesNotExist:
            tag = Tag.objects.create(tname=tag_name)
        PictoTag.objects.create(pid=result, tag_id=tag)
    print(result.img)
    return JsonResponse({'ret': 0, 'msg': '上传成功', 'url': result.img.url, 'id': result.pid})


def delpic(request):
    pid = request.content_params['pid']
    record = Picture.objects.get(pid=pid)
    record.delete()
    return JsonResponse({'ret': 0, 'msg': '删除成功'})


def listPic(request):
    pic = Picture.objects.filter()
    piclist = [{'pid': i.pid,
                'uploader': i.uploader.username,
                'upload_time': i.upload_time.date(),
                'num_like': i.num_like,
                'num_star': i.num_star,
                'num_view': i.num_view,
                'url': i.img.url,
                'width': i.img.width,
                'height': i.img.height, } for i in pic]
    return JsonResponse({'ret': 0, 'picList': piclist})


def favor(request):
    nickname = get_name_from_token(request)
    pid = request.content_params['pid']
    user = User.objects.get(username=nickname)
    pic = Picture.objects.get(pid=pid)
    try:
        favor_pic = Favorite.objects.get(user=user, pid=pic)
    except Favorite.DoesNotExist:
        result = Favorite.objects.create(user=user, pid=pic)
        pic.num_star += 1
        pic.save()
        return JsonResponse({'ret': 0, 'msg': '收藏成功', 'pic': pic.pid, 'num_star': pic.num_star})

    favor_pic.delete()
    pic.num_star -= 1
    pic.save()
    return JsonResponse({'ret': 0, 'msg': '取消收藏', 'pic': pic.pid, 'num_star': pic.num_star})


# def nofavor(request):
#     nickname = get_name_from_token(request)
#     pic = request.content_params['pic']
#     record = Favorite.objects.get(user=nickname, pid=pic)
#     record.delete()
#     img = Picture.objects.get(pid=pic)
#     img.num_star -= 1
#     img.save()
#     return JsonResponse({'ret': 0, 'msg': '删除成功'})


def like(request):
    pid = request.content_params['pid']
    record = Picture.objects.get(pid=pid)
    record.num_like += 1
    record.save()
    return JsonResponse({'ret': 0, 'msg': '点赞成功', 'num_like': record.num_like})


# def addview(request):
#     pid = request.params['pid']
#     record = Picture.objects.get(pid=pid)
#     record.num_view += 1
#     record.save()
#     return JsonResponse({'ret': 0, 'msg': '浏览数增加', 'num_view': record.num_view})


def buildlist(pic):
    plist = [{'pid': i.pid,
              'uploader': i.uploader.username,
              'upload_time': i.upload_time.date(),
              'num_like': i.num_like,
              'num_star': i.num_star,
              'num_view': i.num_view,
              'url': i.img.url,
              'width': i.img.width,
              'height': i.img.height, } for i in pic]
    return plist


def picinfo(request):
    pid = request.content_params['pid']
    picture = Picture.objects.get(pid=pid)
    info = {'pid': picture.pid,
            'name': picture.imgname,
            'uploader': picture.uploader.username,
            'upload_time': picture.upload_time.date(),
            'num_like': picture.num_like,
            'num_star': picture.num_star,
            'num_view': picture.num_view,
            'url': picture.img.url,
            'width': picture.img.width,
            'height': picture.img.height, }
    tags = PictoTag.objects.filter(pid=picture.pid)
    s = ""
    for t in tags:
        s += t.tag_id.tname + ", "
    return JsonResponse({'ret': 0, 'info': info, 'tags': s})


def nameListpic(request):
    pic = Picture.objects.order_by('imgname')
    piclist = buildlist(pic)
    return JsonResponse({'ret': 0, 'picList': piclist})


def dateListpic(request):
    pic = Picture.objects.order_by('upload_time')
    piclist = buildlist(pic)
    return JsonResponse({'ret': 0, 'picList': piclist})


def idListpic(request):
    piclist = Picture.objects.order_by('pid')
    piclist = buildlist(piclist)
    return JsonResponse({'ret': 0, 'picList': piclist})


def likeListpic(request):
    piclist = Picture.objects.order_by('-num_like')
    piclist = buildlist(piclist)
    return JsonResponse({'ret': 0, 'picList': piclist})


def starListpic(request):
    piclist = Picture.objects.order_by('-num_star')
    piclist = buildlist(piclist)
    return JsonResponse({'ret': 0, 'picList': piclist})


def check_user_upload(request):
    username = get_name_from_token(request)
    pid = request.content_params['pid']
    pic = Picture.objects.get(pid=pid)
    if pic.uploader.username == username:
        return JsonResponse({'ret': 0})
    return JsonResponse({'ret': 1})


def user_upload(request):
    username = get_name_from_token(request)
    user = User.objects.get(username=username)
    pic = Picture.objects.filter(uploader=user.id)
    piclist = buildlist(pic)
    return JsonResponse({'ret': 0, 'picList': piclist})


def user_favor(request):
    username = get_name_from_token(request)
    user = User.objects.get(username=username)
    pic = Favorite.objects.filter(user=user.id)
    piclist = []
    for item in pic:
        i = item.pid
        dic = {'pid': i.pid,
               'uploader': i.uploader.username,
               'upload_time': i.upload_time.date(),
               'num_like': i.num_like,
               'num_star': i.num_star,
               'num_view': i.num_view,
               'url': i.img.url,
               'width': i.img.width,
               'height': i.img.height, }
        piclist.append(dic)
    return JsonResponse({'ret': 0, 'picList': piclist})


def tagTopic(request):
    tag = request.content_params['tag']
    try:
        tag_id = Tag.objects.get(tname=tag)
    except Tag.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': '标签不存在'})

    pidlist = PictoTag.objects.filter(tag_id=tag_id)
    piclist = Picture.objects.filter(pid=pidlist.pid)
    piclist = buildlist(piclist)
    return JsonResponse({'ret': 0, 'msg': '为您找到匹配该标签的图片', 'picList': piclist})


def userTopic(request):
    username = request.content_params['user']
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': '用户不存在'})

    piclist = Picture.objects.filter(uploader=user.uid)
    piclist = buildlist(piclist)
    return JsonResponse({'ret': 0, 'msg': '为您找到该用户上传的图片', 'picList': piclist})
