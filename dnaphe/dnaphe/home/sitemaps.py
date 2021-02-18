# from django.contrib import sitemaps
# from django.urls import reverse
#
# class StaticViewSitemap(sitemaps.Sitemap):
#     priority = 0.5
#     changefreq = 'daily'
#
#     def items(self):
#         return ['main', 'about', 'license']
#
#     def location(self, item):
#         return reverse(item)

from django.contrib.sitemaps import Sitemap
from home.models import Post

class dnapheSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.date_posted

    def location(self, obj):
        return ('/post/%s' %obj.pk)