from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from .service.managers import UserManager
from django.utils import timezone


class UserInfo(AbstractBaseUser, PermissionsMixin):
    username = models.EmailField(_('邮件'), max_length=50, default='', unique=True)
    first_name = models.CharField(_('姓'), max_length=50, default='', blank=True, null=False)
    last_name = models.CharField(_('名'), max_length=50, default='')
    mobile = models.CharField(_("手机"), max_length=11, blank=True, null=True)
    img = models.ImageField(_("头像"), upload_to='static/img/users/',
                            default='/avatar/100_1.jpg', null=False, blank=False)
    department = models.ForeignKey('Department', verbose_name="部门", blank=True, on_delete=False)
    is_active = models.BooleanField(_("有效"), default=True)
    is_staff = models.BooleanField(_("员工"), default=True)
    create_date = models.DateTimeField(_('创建日期'), auto_now_add=True)
    roles = models.ManyToManyField(verbose_name='具有的所有角色', to="Role", blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile', 'department', 'is_active', 'is_superuser']

    object = UserManager()

    class Meta:
        verbose_name_plural = _("User")

    def __str__(self):
        return self.username


class Role(models.Model):
    """
    角色表
   CEO
   CTO
   UFO
   销售主管
   销售员
    """
    title = models.CharField(verbose_name='角色名称', max_length=32, unique=True)
    permission = models.ManyToManyField(verbose_name='拥有权限', to="Permission")
    create_date = models.DateTimeField(_('创建日期'), auto_now_add=True)

    def __str__(self):
        return self.title


class Menu(models.Model):
    type_choice = {
        ("system", "系统菜单"),
        ("general", "一般菜单"),
        ("current", "当前用户")}
    name = models.CharField(verbose_name="菜单名称", max_length=32, unique=True)
    types = models.CharField(verbose_name="菜单种类", choices=type_choice, default="select", max_length=50)
    create_date = models.DateTimeField(_('创建日期'), auto_now_add=True)

    def __str__(self):
        return self.name


class PermissionGroup(models.Model):
    """
    权限组
   用户权限组
                用户列表
   主机权限组
                主机列表
    """
    name = models.CharField(max_length=32, unique=True)
    menu = models.ForeignKey(verbose_name='所属菜单', to='Menu', on_delete=False)
    create_date = models.DateTimeField(_('创建日期'), auto_now_add=True)

    def __str__(self):
        return self.name


class Permission(models.Model):
    """
    权限表
                                                                                组内菜单ID
    用户列表      /users/                 list               1            null
    添加用户      /users/add/             add                1            1
    删除用户      /users/del/(\d+)/       del                1            1
    修改用户      /users/edit/(\d+)/      edit               1            1
    主机列表      /hosts/                 list               2            null
    添加主机      /hosts/add/             add                2             5
    删除主机      /hosts/del/(\d+)/       del                2             5
    修改主机      /hosts/edit/(\d+)/      edit               2             5

    以后获取当前用户权限后，数据结构化处理，并放入session
    {
        1: {
            urls: [/users/,/users/add/ ,/users/del/(\d+)/],
            codes: [list,add,del]
        },
        2: {
            urls: [/hosts/,/hosts/add/ ,/hosts/del/(\d+)/],
            codes: [list,add,del]
        }
    }


    """
    code_choice = {
        ("insert", "添加"),
        ("delete", "删除"),
        ("select", "查看"),
        ("update", "修改")
    }
    title = models.CharField(verbose_name='权限名称', max_length=32, unique=True)
    code = models.CharField(verbose_name="读写情况", choices=code_choice, default="select", max_length=50)
    group = models.ForeignKey(verbose_name='所属权限组', to="PermissionGroup", on_delete=False)
    url = models.CharField(verbose_name='含正则的URL', max_length=255)
    # is_menu = models.BooleanField(verbose_name='是否是菜单')
    group_menu = models.ForeignKey(verbose_name='组内菜单', to="Permission", null=True, blank=True, related_name='权限',
                                   on_delete=False)
    create_date = models.DateTimeField(_('创建日期'), auto_now_add=True)

    def __str__(self):
        return self.title


class Department(models.Model):
    """
    部门
    """
    title = models.CharField(max_length=32, unique=True)
    create_date = models.DateTimeField(_(u'创建日期'), auto_now_add=True)

    def __str__(self):
        return self.title
