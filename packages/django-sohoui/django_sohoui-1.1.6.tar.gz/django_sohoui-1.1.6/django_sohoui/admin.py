from django.contrib import admin
from .adminsite import adminsite   
from .models import AdminMenus

class AdminMenusAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'icon', 'parent_id', 'sort', 'is_show')
    list_filter = ('parent_id', 'is_show')
    search_fields = ('name', 'url')
    ordering = ('sort',)

adminsite.register(AdminMenus, AdminMenusAdmin)