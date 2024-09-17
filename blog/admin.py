from django.contrib import admin

from blog.models import Blog


# Register your models here.
@admin.register(Blog)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
