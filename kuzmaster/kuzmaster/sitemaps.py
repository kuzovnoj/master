from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    protocol = 'https'

    items = ['home', 'gallery:gallery', 'works:price_list']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        if item == 'home':
            return 1.0
        return 0.8

    def changefreq(self, item):
        if item == 'home':
            return 'weekly'
        return 'monthly'
