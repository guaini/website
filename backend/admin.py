from django.contrib import admin
from backend.models import Picture, User, Favorite, Tag, PictoTag

# Register your models here.
admin.site.register(Picture)
admin.site.register(User)
admin.site.register(Favorite)
admin.site.register(Tag)
admin.site.register(PictoTag)
