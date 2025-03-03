from django.contrib import admin

from .models import Category, Article, Comment, Tags, ArticleTags, ArticleImages, CustomUser

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Tags)
admin.site.register(ArticleTags)
admin.site.register(ArticleImages)
admin.site.register(CustomUser)