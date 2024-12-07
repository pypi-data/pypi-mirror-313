from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy

from django.conf import settings

def custom_context(request):
    return {
        # 登录背景图片
        'LOGIN_BG_IMAGE': settings.LOGIN_BG_IMAGE,
        # 站点标题
        'site_header': settings.SITE_HEADER,
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
    # Text to put at the end of each page's <title>.
    site_title = gettext_lazy("Django site admin")

    # Text to put in each page's <div id="site-name">.
    site_header = gettext_lazy("Django administration")

    # Text to put at the top of the admin index page.
    index_title = gettext_lazy("Site administration")

    # URL for the "View site" link at the top of each admin page.
    site_url = "/"

    enable_nav_sidebar = True

    # 登录页&首页的标题
    site_header = '登录页&首页的标题'
    # 浏览器的标题
    site_title = '浏览器的标题'
    # 正文的标题
    index_title = '正文的标题'
    
    
    # 登录页
    # login_template = ''
    
    
adminsite = MyAdminSite()


# 注册用户模型
adminsite.register(User, UserAdmin)

# 注册组模型
class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ['permissions']

adminsite.register(Group, GroupAdmin)