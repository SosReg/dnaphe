from django.contrib import admin
from .models import Post, Comment, Lang_tag, Topic, T_Jobs

# Register your models here.

admin.site.register(Topic)
admin.site.register(Lang_tag)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(T_Jobs)