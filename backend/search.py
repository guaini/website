from django.http import JsonResponse

from backend.models import User, Picture, PictoTag, Tag
from backend.views import buildlist


def search(request):
    key_words = request.GET.get('key')
    # key_words = request.content_params['key']
    key_words = key_words.split(" ")
    key_words = list(set(key_words))  # 关键词去重
    pid_ls = []
    pname_ls = []
    tag_ls = []
    artist_ls = []
    pic = None

    for i, s in enumerate(key_words):
        key, value = s.split("=")
        if key == 'pid':
            pid_ls.append(value)
            continue

        if key == 'pname':
            pname_ls.append(value)
            continue

        if key == 'tag':
            tag_ls.append(value)
            continue

        if key == 'uploader':
            artist_ls.append(value)
            continue

    if len(pid_ls) != 0:
        tmp = []
        for i in range(len(pid_ls)):
            p = Picture.objects.filter(pid=pid_ls[i])
            if not p:
                return JsonResponse({'ret': 1, 'msg': '!'})
            tmp.extend(p)
        if pic is None:
            pic = tmp
        else:
            pic = list(set(pic).intersection(set(tmp)))
            if not pic:
                return JsonResponse({'ret': 1, 'msg': '没有符合条件的图片!'})
        # piclist = buildlist(pic)
        # return JsonResponse({'ret': 0, 'msg': '根据您输入的 pid 为您找到', 'picList': piclist})

    if len(pname_ls) != 0:
        p = []
        for i in range(len(pname_ls)):
            pt = Picture.objects.filter(imgname=pname_ls[i])
            if not pt:
                return JsonResponse({'ret': 1, 'msg': '请输入正确的 pname!'})
            p.extend(pt)

        if pic is None:
            pic = p
        else:
            pic = list(set(pic).intersection(set(p)))
            if not pic:
                return JsonResponse({'ret': 1, 'msg': '没有符合条件的图片!'})

    if len(tag_ls) != 0:
        p = []
        for i in range(len(tag_ls)):
            try:
                tag = Tag.objects.get(tname=tag_ls[i])
            except Tag.DoesNotExist:
                return JsonResponse({'ret': 1, 'msg': '请输入正确的标签！'})

            pt = PictoTag.objects.filter(tag_id=tag)
            plist = []
            for img in pt:
                plist.append(img.pid)
            if not pt:
                return JsonResponse({'ret': 1, 'msg': '没有符合条件的图片!'})

            if not p:
                p = plist
            else:
                p = list(set(p).intersection(set(pt)))
                if p is []:
                    return JsonResponse({'ret': 1, 'msg': '请输入正确的标签!'})

        if pic is None:
            pic = p
        else:
            pic = list(set(pic).intersection(set(p)))
            if not pic:
                return JsonResponse({'ret': 1, 'msg': '没有符合条件的图片!'})

    if len(artist_ls) != 0:
        if len(artist_ls) > 1:
            return JsonResponse({'ret': 1, 'msg': '搜索的作者数不能多于一个!'})
        try:
            user = User.objects.get(username=artist_ls[0])
        except User.DoesNotExist:
            return JsonResponse({'ret': 1, 'msg': '请输入正确的作者名!'})

        p = Picture.objects.filter(uploader=user)
        if p is []:
            return JsonResponse({'ret': 1, 'msg': '没有符合条件的图片!'})

        if pic is None:
            pic = p
        else:
            pic = list(set(pic).intersection(set(p)))

    if pic is not None or pic != []:
        piclist = buildlist(pic)
        return JsonResponse({'ret': 0, 'msg': '为您搜索到以下图片', 'picList': piclist})
    else:
        return JsonResponse({'ret': 1, 'msg': '没有符合条件的图片!'})
