from django.contrib import admin
from django.forms import Textarea
from blog.models import Blog,Contact, Technology
from django.contrib.auth import get_user_model

User = get_user_model()


class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_at", "status")
    list_filter = ("status", "created_at", "published_at", "author")
    search_fields = ("title", "content")
    raw_id_fields = ("author",)
    date_hierarchy = "published_at"
    ordering = ("status", "-published_at")
    formfield_overrides = {
    Blog.contents: {'widget': Textarea(
                       attrs={'rows': 1,
                              'cols': 40})},
}

class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "platform", "slug")
    prepopulated_fields = {"slug": ("slug",)}  # new



admin.site.register(Blog, BlogAdmin)
admin.site.register(Contact)
admin.site.register(Technology,TechnologyAdmin)