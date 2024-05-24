from django.contrib import admin
from .models import Posts, Category

class PostsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Posts._meta.get.fields()]




admin.site.register(Posts)
admin.site.register(Category)
# Register your models here.
