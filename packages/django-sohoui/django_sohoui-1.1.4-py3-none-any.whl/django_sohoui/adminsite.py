from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy

from django.conf import settings

def custom_context(request):
    return {
        # 登录背景图片
        'LOGIN_BG_IMAGE': settings.SOHO_LOGIN_BG_IMAGE,
        # 站点标题
        'site_header': settings.SOHO_SITE_HEADER,
        'app_list': [
                {      'name': '认证和授权',
            'app_label': 'auth',
            'app_url': '/admin/auth/',
            'has_module_perms': True,
            'models': [
            {
                'model': 'django.contrib.auth.models.User',
                'name': '用户',
                'object_name': 'User',
                'perms':
                {
                    'add': False,
                    'change': False,
                    'delete': False,
                    'view': True
                },
                'admin_url': '/admin/auth/user/',
                'add_url': None,
                'view_only': True
            },
            {
                'model': 'django.contrib.auth.models.Group',
                'name': '组',
                'object_name': 'Group',
                'perms':
                {
                    'add': True,
                    'change': True,
                    'delete': True,
                    'view': True
                },
                'admin_url': '/admin/auth/group/',
                'add_url': '/admin/auth/group/add/',
                'view_only': False
                }]
            }
        ]
    }
    
    

class MyAdminSite(admin.AdminSite):

    # URL for the "View site" link at the top of each admin page.
    site_url = "/"

    enable_nav_sidebar = True

    # 登录页&首页的标题
    site_header = '登录页&首页的标题'
    # 浏览器的标题
    site_title = '浏览器的标题'
    # 正文的标题
    index_title = '正文的标题'
    
    
    # def each_context(self, request):
    #     """
    #     Return a dictionary of variables to put in the template context for
    #     *every* page in the admin site.

    #     For sites running on a subpath, use the SCRIPT_NAME value if site_url
    #     hasn't been customized.
    #     """
    #     script_name = request.META["SCRIPT_NAME"]
    #     site_url = (
    #         script_name if self.site_url == "/" and script_name else self.site_url
    #     )
    #     return {
    #         "site_title": self.site_title,
    #         "site_header": self.site_header,
    #         "site_url": site_url,
    #         "has_permission": self.has_permission(request),
    #         "available_apps": self.get_app_list(request),
    #         "is_popup": False,
    #         "is_nav_sidebar_enabled": self.enable_nav_sidebar,
    #         "log_entries": self.get_log_entries(request),
    #     }
        
    # from django.template import RequestContext
    # from project.context_processors import custom_context
    # custom_context = custom_context(RequestContext(request))
    # context['app_list'] = custom_context['app_list']
    
adminsite = MyAdminSite()


# 注册用户模型
adminsite.register(User, UserAdmin)

# 注册组模型
class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ['permissions']

adminsite.register(Group, GroupAdmin)