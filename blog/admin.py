from django.contrib import admin
from blog.models import Public



@admin.register(Public)
class PublicAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    list_filter = ('available',)
    search_fields = ('name', 'description',)



