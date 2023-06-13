import json

from django.http import JsonResponse, HttpRequest

from backend.views import like, favor, listPic, delpic, verify


def dispatcher(request: HttpRequest):
    if request.method == 'GET':
        request.content_params = request.GET

    elif request.method in ['POST', 'PUT', 'DELETE']:
        request.content_params = json.loads(request.body)
    action = request.content_params['action']

    print(action)
    if action == 'like':
        if verify(request) == 0:
            return JsonResponse({'ret': 1, 'msg': '未登录'})
        return like(request)
    elif action == 'favor':
        if verify(request) == 0:
            return JsonResponse({'ret': 1, 'msg': '未登录'})
        return favor(request)
    # elif action == 'nofavor':
    #     if verify(request) == 0:
    #         return JsonResponse({'ret': 1, 'msg': '未登录'})
    #     return nofavor(request)
    elif action == 'list':
        return listPic(request)
    elif action == 'delete':
        if verify(request) == 0:
            return JsonResponse({'ret': 1, 'msg': '未登录'})
        return delpic(request)
    # elif action == 'view':
    #     return addview(request)
    else:
        return JsonResponse({'ret': 1, 'msg': '未找到处理该请求的方法'})
