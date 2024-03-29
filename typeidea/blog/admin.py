from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Tag, Category, Post
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'owner', 'created_time', 'post_count']
    fields = ['name', 'status', 'is_nav']

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'

    def get_queryset(self, request):
        qs = super(CategoryAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'owner', 'created_time']
    fields = ['name', 'status']

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(TagAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'desc', 'status', 'category', 'tag', 'created_time', 'operator']
    list_display_links = []

    list_filter = ['category']
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    # save_on_top = True

    fields = (
        ('category', 'title'),
        'tag',
        'desc',
        'status',
        'content',
    )

    def operator(self, obj):
        return format_html(
            '<a href={}>编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id, ))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
