from django.http import JsonResponse
import json
from backend.views import dateListpic, idListpic, likeListpic, starListpic, tagTopic, userTopic, nameListpic, \
    user_upload, user_favor, picinfo, check_user_upload, verify


def dispatcher(request):
    if request.method == 'GET':
        request.content_params = request.GET

    action = request.content_params['action']

    if action == 'date':
        return dateListpic(request)
    elif action == 'pid':
        return idListpic(request)
    elif action == 'like':
        return likeListpic(request)
    elif action == 'star':
        return starListpic(request)
    elif action == 'tag':
        return tagTopic(request)
    elif action == 'user':
        return userTopic(request)
    elif action == 'name':
        return nameListpic(request)
    elif action == 'upload_list':
        if verify(request) == 0:
            return JsonResponse({'ret': 1, 'msg': '未登录'})
        return user_upload(request)
    elif action == 'favor_list':
        if verify(request) == 0:
            return JsonResponse({'ret': 1, 'msg': '未登录'})
        return user_favor(request)
    elif action == 'pic_info':
        return picinfo(request)
    elif action == 'check_upload':
        if verify(request) == 0:
            return JsonResponse({'ret': 1, 'msg': '未登录'})
        return check_user_upload(request)
    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})
