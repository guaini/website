import json

from django.http import JsonResponse, HttpRequest

from backend.views import adduser, signin, update, verify, signout, userInfo


def dispatcher(request: HttpRequest):
    if request.method == 'GET':
        request.content_params = request.GET

    elif request.method in ['POST', 'PUT', 'DELETE']:
        request.content_params = json.loads(request.body)
    action = request.content_params['action']

    print(action)
    if action == 'login':
        if verify(request) == 1:
            return JsonResponse({'ret': 1, 'msg': '请勿重复登录'})
        return signin(request)
    elif action == 'register':
        if verify(request) == 1:
            return JsonResponse({'ret': 1, 'msg': '已登录'})
        return adduser(request)
    elif action == 'logout':
        if verify(request) == 0:
            return JsonResponse({'ret': 1, 'msg': '未登录或登录超时'})
        return signout(request)
    elif action == 'update':
        if verify(request) == 0:
            return JsonResponse({'ret': 1, 'msg': '未登录'})
        return update(request)
    elif action == 'getinfo':
        if verify(request) == 0:
            return JsonResponse({'ret': 1, 'msg': '未登录'})
        return userInfo(request)
    else:
        return JsonResponse({'ret': 1, 'msg': '未找到处理该请求的方法'})
