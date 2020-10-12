from django.contrib import admin

from api.models import Video, Channel, Like, Dislike, Platform, Watched, Browser

# Register your models here.
admin.site.register(Video)
admin.site.register(Channel)
admin.site.register(Platform)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Watched)
admin.site.register(Browser)

