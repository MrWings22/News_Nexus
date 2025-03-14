from django.contrib import admin

from .models import Category, Article, Comment, Tags, ArticleTags, ArticleImages, CustomUser
class ArticlAdmin(admin.ModelAdmin):
    list_display = ['head_line', 'category', 'user', 'created_at', 'updated_at']
    list_filter = ['category', 'user', 'created_at', 'updated_at']
    search_fields = ['head_line', 'description', 'user__username', 'category__category_name']
    list_per_page = 10
    readonly_fields = ["views"]
admin.site.register(Category)
admin.site.register(Article, ArticlAdmin)
admin.site.register(Comment)
admin.site.register(Tags)
admin.site.register(ArticleTags)
admin.site.register(ArticleImages)
admin.site.register(CustomUser)