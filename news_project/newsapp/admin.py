from django.contrib import admin
from .models import Category, Article, Comment, Tags, ArticleTags, ArticleImages, CustomUser, Subscriber

class ArticlAdmin(admin.ModelAdmin):
    list_display = ['head_line', 'category', 'user', 'created_at', 'updated_at']
    list_filter = ['category', 'user', 'created_at', 'updated_at']
    search_fields = ['head_line', 'description', 'user__username', 'category__category_name']
    list_per_page = 10
    readonly_fields = ["views","user"]

    def save_model(self, request, obj, form, change):
        if not change or not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if obj is None:
            # this is the Add form, populate user field manually
            fields.remove('user')
        return fields

    def get_changeform_initial_data(self, request):
        return {'user': request.user}



admin.site.register(Category)
admin.site.register(Article, ArticlAdmin)
admin.site.register(Comment)
admin.site.register(Tags)
admin.site.register(ArticleTags)
admin.site.register(ArticleImages)
admin.site.register(CustomUser)
admin.site.register(Subscriber)

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email',)  # Show emails in the admin panel
    search_fields = ('email',)  # Enable search by email
    filter_horizontal = ('categories',)  


    

