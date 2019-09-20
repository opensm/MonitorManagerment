# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
import uuid
import os
from PIL import Image

from .forms import *
from .models import *
from rbac.service.init_permission import *


def crop_image(avatar, uid):
    """
    :param avatar:
    :param uid:
    :return:
    """
    # 生成UUID文件名和对应路径
    ext = avatar.name.split('.')[-1]
    avatar_name = '{}.{}'.format(uuid.uuid4().hex[:16], ext)
    # 相对路径
    cropped_avatar = os.path.join("avatar", str(uid), avatar_name)
    # 对应根目录路径
    avatar_absolute_path = os.path.join('upload', 'avatar', str(uid))
    avatar_absolute_file = os.path.join(avatar_absolute_path, avatar_name)
    if not os.path.exists(avatar_absolute_path):
        os.makedirs(avatar_absolute_path, 740)
    # 裁剪图片
    try:
        images = Image.open(avatar)
        crop_img = images.resize((100, 100), Image.ANTIALIAS)
        crop_img.save(avatar_absolute_file)
        return {"img_name": cropped_avatar, "status": True, "msg": "success"}
    except Exception as error:
        return {"img_name": cropped_avatar, "status": False, "msg": str(error)}


# 用户模块 ########################
# 登陆
class UserLoginView(View):
    template_name = 'rbac/login.html'

    def post(self, request):

        if request.user.is_authenticated:
            return redirect('index')
        login = LoginForm(request.POST)
        if not login.is_valid():
            return render(request, self.template_name, {'login': login})

        try:
            data = login.cleaned_data
            user = auth.authenticate(username=data['username'], password=data['password'])
            if user is None or not user.is_active:
                raise Exception(_("Wrong account or password"))
            auth.login(request, user)
            init_permission(user=user, request=request)
            return redirect('index')
        except Exception as errors:
            return render(request, self.template_name, {
                'login': login,
                "errors": errors
            })

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        login = LoginForm()
        return render(request, self.template_name, {'login': login})


# 修改密码
class CurrentUserPasswordReset(View):
    template_name = 'rbac/password.html'
    view_message = "修改密码"

    @method_decorator(login_required())
    def post(self, request):
        password_reset = PasswordReset(user=request.user, data=request.POST)
        if not password_reset.is_valid():
            return render(request, self.template_name, {'password_reset': password_reset})
        password_reset.save()
        update_session_auth_hash(request, password_reset.user)
        return redirect('rbac:users')

    @method_decorator(login_required())
    def get(self, request):
        password_reset = PasswordReset(user=request.user)
        # password_reset = PasswordReset()
        return render(request, self.template_name, {
            'password_reset': password_reset,
            "view_message": self.view_message
        })


# 退出
class UserLogoutView(View):

    @method_decorator(login_required)
    def post(self, request):
        auth.logout(request)
        return HttpResponseRedirect(reverse("rbac:login"))

    @method_decorator(login_required)
    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect(reverse("rbac:login"))


# 用户列表
class UserListView(View):
    template_name = 'rbac/user.html'
    view_message = "用户列表"

    @method_decorator(login_required)
    def get(self, request):
        user_list = UserInfo.object.order_by('create_date')
        return render(request, self.template_name, {
            'user_list': user_list,
            "view_message": self.view_message
        })

    @method_decorator(login_required)
    def post(self, request):
        user_list = UserInfo.object.order_by('create_date')
        return render(request, self.template_name, {
            'user_list': user_list,
            "view_message": self.view_message
        })


# 用户编辑
class UserEditView(View):
    template_name = 'rbac/user_edit.html'
    view_message = "修改用户"

    @method_decorator(login_required)
    def post(self, request, user_id):
        user_detail = get_object_or_404(UserInfo, pk=user_id)
        user_form = UserProfixForm(request.POST, request.FILES, instance=user_detail)
        if not user_form.is_valid():
            return render(request, self.template_name, {
                'user_form': user_form,
                "view_message": self.view_message
            })
        img_edit = user_form.save(commit=False)
        if "img" in request.FILES:
            avatar_edit_result = crop_image(request.FILES['img'], user_id)
            if not avatar_edit_result['status']:
                return render(request, self.template_name, {
                    'user_form': user_form,
                    "view_message": self.view_message,
                    "error": avatar_edit_result["msg"]
                })
            else:
                img_edit.img = avatar_edit_result['img_name']
        img_edit.save()
        return redirect('rbac:users')

    @method_decorator(login_required)
    def get(self, request, user_id):
        user_detail = get_object_or_404(UserInfo, pk=user_id)
        user_form = UserProfixForm(instance=user_detail)
        return render(request, self.template_name, {
            'user_form': user_form,
            "view_message": self.view_message
        })


# 删除用户
class UserDelView(View):
    template_name = 'rbac/user.html'

    @method_decorator(login_required)
    def post(self, request, user_id):
        try:
            UserInfo.object.get(pk=user_id).delete()
            return redirect('rbac:users')
        except Exception as error:
            user_list = UserInfo.object.order_by('create_date')
            return render(request, self.template_name, {
                'user_list': user_list,
                'error': error
            })

    @method_decorator(login_required())
    def get(self, request, user_id):
        try:
            UserInfo.object.get(pk=user_id).delete()
            return redirect('rbac:users')
        except Exception as error:
            user_list = UserInfo.object.order_by('create_date')
            return render(request, self.template_name, {
                'user_list': user_list,
                'error': error
            })


# 添加用户
class UserRegisterView(View):
    template_name = 'rbac/user_edit.html'
    view_message = "添加用户"

    @method_decorator(login_required)
    def post(self, request):
        """
        :param request:
        :return:
        """
        user_register = UserProfixForm(request.POST)
        if not user_register.is_valid():
            return render(request, self.template_name, {
                'user_form': user_register,
                "view_message": self.view_message
            })
        try:
            user_register.save()
            user_data = UserInfo.object.get(username=user_register.cleaned_data['username'])
            if "img" in request.FILES:
                avatar_edit_result = crop_image(request.FILES['img'], user_data.id)
                if not avatar_edit_result['status']:
                    return render(request, self.template_name, {
                        'user_form': user_register,
                        "view_message": self.view_message,
                        "error": avatar_edit_result["msg"]
                    })
                else:
                    user_data.img = avatar_edit_result['img_name']
                user_data.set_password("dkmgame123")
                user_data.save()
            return redirect('rbac:users')
        except Exception as error:
            return render(request, self.template_name, {
                'user_form': user_register,
                'error': error,
                "view_message": self.view_message
            })

    @method_decorator(login_required)
    def get(self, request):
        user_register = UserProfixForm()
        return render(request, self.template_name, {
            'user_form': user_register,
            "view_message": self.view_message
        })


# 角色模块 ########################
# 角色列表
class RoleListView(View):
    template_name = 'rbac/role.html'
    view_message = "角色列表"

    @method_decorator(login_required)
    def post(self, request):
        role_list = Role.objects.order_by('title')
        return render(request, self.template_name, {
            "role_list": role_list,
            "view_message": self.view_message
        })

    @method_decorator(login_required)
    def get(self, request):
        role_list = Role.objects.order_by('title')
        return render(request, self.template_name, {
            "role_list": role_list,
            "view_message": self.view_message
        })


# 添加角色
class RoleRegisterView(View):
    template_name = 'rbac/role_edit.html'
    view_message = "添加角色"

    @method_decorator(login_required)
    def post(self, request):
        role_register = RoleInfoModelForm(request.POST)
        if not role_register.is_valid():
            return render(request, self.template_name, {
                "role_register": role_register,
                "view_message": self.view_message
            })
        try:
            role_register.save()
            return redirect('rbac:roles')
        except Exception as error:
            return render(request, self.template_name, {
                "role_register": role_register,
                "view_message": self.view_message,
                'error': error
            })

    @method_decorator(login_required)
    def get(self, request):
        role_register = RoleInfoModelForm()
        return render(request, self.template_name, {
            'role_register': role_register,
            "view_message": self.view_message
        })


class RoleEditView(View):
    template_name = 'rbac/role_edit.html'
    view_message = "编辑角色"

    @method_decorator(login_required)
    def post(self, request, role_id):
        role_data = get_object_or_404(Role, pk=role_id)
        role_register = RoleInfoModelForm(request.POST, instance=role_data)
        if not role_register.is_valid():
            return render(request, self.template_name, {
                "role_register": role_register,
                "view_message": self.view_message
            })
        try:
            role_register.save(commit=True, create=False)
            return redirect('rbac:roles')
        except Exception as error:
            return render(request, self.template_name, {
                "role_register": role_register,
                "view_message": self.view_message,
                "error": error
            })

    @method_decorator(login_required)
    def get(self, request, role_id):
        role_data = get_object_or_404(Role, pk=role_id)
        role_register = RoleInfoModelForm(instance=role_data)
        return render(request, self.template_name, {
            "role_register": role_register,
            "view_message": self.view_message
        })


class RoleDelView(View):
    template_name = 'rbac/role.html'
    view_message = "删除角色"

    @method_decorator(login_required)
    def post(self, request, role_id):
        try:
            Role.objects.get(pk=role_id).delete()
            return redirect('rbac:roles')
        except Exception as error:
            role_list = Role.objects.order_by('title')
            return render(request, self.template_name, {
                'role_list': role_list,
                'error': error
            })


# 菜单管理 ###############################
# 添加菜单
class MenuRegisterView(View):
    template_name = "rbac/menu_edit.html"
    view_message = "添加菜单"

    @method_decorator(login_required)
    def post(self, request):
        menu_register = MenuInfoForm(request.POST)
        if not menu_register.is_valid():
            return render(request, self.template_name, {
                "menu_register": menu_register,
                "view_message": self.view_message
            })
        try:
            menu_register.save()
            return redirect('rbac:menu')
        except Exception as error:
            return render(request, self.template_name, {
                "menu_register": menu_register,
                "view_message": self.view_message,
                "error": error
            })

    @method_decorator(login_required)
    def get(self, request):
        menu_register = MenuInfoForm()
        return render(request, self.template_name, {
            "menu_register": menu_register,
            "view_message": self.view_message
        })


# 菜单列表
class MenuListView(View):
    template_name = "rbac/menu_site.html"
    view_message = "菜单列表"

    @method_decorator(login_required)
    def post(self, request):
        menu_data = Menu.objects.order_by('create_date')
        return render(request, self.template_name, {
            "menu_data": menu_data,
            "view_message": self.view_message
        })

    @method_decorator(login_required)
    def get(self, request):
        menu_data = Menu.objects.order_by('create_date')
        return render(request, self.template_name, {
            "menu_data": menu_data,
            "view_message": self.view_message
        })


# 编辑菜单信息
class MenuEditView(View):
    template_name = 'rbac/menu_edit.html'
    view_message = "修改菜单信息"

    @method_decorator(login_required)
    def post(self, request, menu_id):
        menu_data = get_object_or_404(Menu, pk=menu_id)
        menu_register = MenuInfoForm(request.POST, instance=menu_data)
        if not menu_register.is_valid():
            return render(request, self.template_name, {
                "menu_register": menu_register,
                "view_message": self.view_message
            })
        try:
            menu_register.save()
            return redirect('rbac:menu')
        except Exception as error:
            return render(request, self.template_name, {
                "menu_register": menu_register,
                "view_message": self.view_message,
                "error": error
            })

    @method_decorator(login_required)
    def get(self, request, menu_id):
        menu_data = get_object_or_404(Menu, pk=menu_id)
        menu_register = MenuInfoForm(instance=menu_data)
        return render(request, self.template_name, {
            "menu_register": menu_register,
            "view_message": self.view_message
        })


# 删除菜单
class MenuDelView(View):
    template_name = 'rbac/menu_site.html'
    view_message = "菜单列表"

    @method_decorator(login_required)
    def post(self, request, menu_id):
        try:
            Menu.objects.get(pk=menu_id).delete()
            return redirect('rbac:menu')
        except Exception as error:
            menu_data = Menu.objects.order_by('id')
            return render(request, self.template_name, {
                "menu_data": menu_data,
                "view_message": self.view_message,
                "error": error
            })

    @method_decorator(login_required)
    def get(self, request, menu_id):
        try:
            Menu.objects.get(pk=menu_id).delete()
            return redirect('rbac:menu')
        except Exception as error:
            menu_data = Menu.objects.order_by('id')
            return render(request, self.template_name, {
                "menu_data": menu_data,
                "view_message": self.view_message,
                "error": error
            })


# 权限组 ###########################
# 权限组列表
class PermissionGroupListView(View):
    template_name = 'rbac/permission_group.html'
    view_message = "权限组列表"

    @method_decorator(login_required)
    def post(self, request):
        permission_group_data = PermissionGroup.objects.order_by('create_date')
        return render(request, self.template_name, {
            "permission_group_data": permission_group_data,
            "view_message": self.view_message
        })

    @method_decorator(login_required)
    def get(self, request):
        permission_group_data = PermissionGroup.objects.order_by('create_date')
        return render(request, self.template_name, {
            "permission_group_data": permission_group_data,
            "view_message": self.view_message
        })


# 修改权限组信息
class PermissionGroupEditView(View):
    template_name = 'rbac/permission_group_edit.html'
    view_message = "修改权限组"

    @method_decorator(login_required)
    def post(self, request, group_id):
        permission_group_data = get_object_or_404(PermissionGroup, pk=group_id)
        permission_group_register = PermissionGroupForm(request.POST, instance=permission_group_data)
        if not permission_group_register.is_valid():
            return render(request, self.template_name, {
                "permission_group_register": permission_group_register,
                "view_message": self.view_message
            })
        try:
            permission_group_register.save()
            return redirect('rbac:permission_group')
        except Exception as error:
            return render(request, self.template_name, {
                "permission_group_register": permission_group_register,
                "view_message": self.view_message,
                "error": error
            })

    @method_decorator(login_required)
    def get(self, request, group_id):
        permission_group_data = get_object_or_404(PermissionGroup, pk=group_id)
        permission_group_register = PermissionGroupForm(instance=permission_group_data)
        return render(request, self.template_name, {
            "permission_group_register": permission_group_register,
            "view_message": self.view_message
        })


# 删除权限组
class PermissionGroupDelView(View):
    template_name = 'rbac/permission_group.html'
    view_message = "修改权限组"

    @method_decorator(login_required)
    def post(self, request, group_id):
        try:
            PermissionGroup.objects.get(pk=group_id).delete()
            return redirect('rbac:permission_group')
        except Exception as error:
            permission_group_data = PermissionGroup.objects.order_by('id')
            return render(request, self.template_name, {
                "permission_group_data": permission_group_data,
                "view_message": self.view_message,
                "error": error
            })


# 添加权限组
class PermissionGroupRegisterView(View):
    template_name = 'rbac/permission_group_edit.html'
    view_message = "添加权限组"

    @method_decorator(login_required)
    def post(self, request):
        permission_group_register = PermissionGroupForm(request.POST)
        if not permission_group_register.is_valid():
            return render(request, self.template_name, {
                "permission_group_register": permission_group_register,
                "view_message": self.view_message
            })
        try:
            permission_group_register.save()
            return redirect('rbac:permission_group')
        except Exception as error:
            return render(request, self.template_name, {
                "permission_group_register": permission_group_register,
                "view_message": self.view_message,
                "error": error
            })

    @method_decorator(login_required)
    def get(self, request):
        permission_group_register = PermissionGroupForm()
        return render(request, self.template_name, {
            "permission_group_register": permission_group_register,
            "view_message": self.view_message
        })


# 权限 ################################
# 添加权限
class PermissionRegisterView(View):
    template_name = 'rbac/permission_edit.html'
    view_message = "添加权限"

    @method_decorator(login_required)
    def post(self, request):
        permission_register = PermissionForm(request.POST)
        if not permission_register.is_valid():
            return render(request, self.template_name, {
                "permission_register": permission_register,
                "view_message": self.view_message
            })
        try:
            permission_register.save()
            return redirect('rbac:permission')
        except Exception as error:
            return render(request, self.template_name, {
                "permission_register": permission_register,
                "view_message": self.view_message,
                "error": error
            })

    @method_decorator(login_required)
    def get(self, request):
        permission_register = PermissionForm()
        return render(request, self.template_name, {
            "permission_register": permission_register,
            "view_message": self.view_message
        })


# 删除权限
class PermissionDelView(View):
    template_name = 'rbac/permission.html'
    view_message = "删除权限"

    @method_decorator(login_required)
    def post(self, request, permission_id):
        try:
            Permission.objects.get(pk=permission_id).delete()
            return redirect('rbac:permission')
        except Exception as error:
            permission_data = Permission.objects.order_by('id')
            return render(request, self.template_name, {
                "permission_data": permission_data,
                "view_message": self.view_message,
                "error": error
            })

    @method_decorator(login_required)
    def get(self, request, permission_id):
        try:
            Permission.objects.get(pk=permission_id).delete()
            return redirect('rbac:permission')
        except Exception as error:
            permission_data = Permission.objects.order_by('id')
            return render(request, self.template_name, {
                "permission_data": permission_data,
                "view_message": self.view_message,
                "error": error
            })


# 权限列表
class PermissionListView(View):
    template_name = 'rbac/permission.html'
    view_message = "权限列表"

    @method_decorator(login_required)
    def post(self, request):
        permission_data = Permission.objects.order_by('create_date')
        return render(request, self.template_name, {
            "permission_data": permission_data,
            "view_message": self.view_message
        })

    @method_decorator(login_required)
    def get(self, request):
        permission_data = Permission.objects.order_by('create_date')
        return render(request, self.template_name, {
            "permission_data": permission_data,
            "view_message": self.view_message
        })


# 修改权限
class PermissionEditView(View):
    template_name = 'rbac/permission_edit.html'
    view_message = "编辑权限"

    @method_decorator(login_required)
    def post(self, request, permission_id):
        permission_data = get_object_or_404(Permission, pk=permission_id)
        permission_register = PermissionForm(request.POST, instance=permission_data)
        if not permission_register.is_valid():
            return render(request, self.template_name, {
                "permission_register": permission_register,
                "view_message": self.view_message
            })
        try:
            permission_register.save()
            return redirect('rbac:permission')
        except Exception as error:
            return render(request, self.template_name, {
                "permission_register": permission_register,
                "view_message": self.view_message,
                "error": error
            })

    @method_decorator(login_required)
    def get(self, request, permission_id):
        permission_data = get_object_or_404(Permission, pk=permission_id)
        permission_register = PermissionForm(instance=permission_data)
        return render(request, self.template_name, {
            "permission_register": permission_register,
            "view_message": self.view_message
        })


# 部门 ################################
# 添加部门
class DepartmentRegisterView(View):
    template_name = "rbac/department_edit.html"
    view_message = "添加部门"

    @method_decorator(login_required)
    def post(self, request):
        department_register = DepartmentForm(request.POST)
        if not department_register.is_valid():
            return render(request, self.template_name, {
                "department_register": department_register,
                "view_message": self.view_message
            })
        try:
            department_register.save()
            return redirect('rbac:department')
        except Exception as error:
            return render(request, self.template_name, {
                "department_register": department_register,
                "view_message": self.view_message,
                "error": error
            })

    @method_decorator(login_required)
    def get(self, request):
        department_register = DepartmentForm()
        return render(request, self.template_name, {
            "department_register": department_register,
            "view_message": self.view_message
        })


# 删除部门
class DepartmentDelView(View):
    template_name = "rbac/department.html"
    view_message = "部门列表"

    @method_decorator(login_required)
    def post(self, request, department_id):
        try:
            Department.objects.get(pk=department_id).delete()
            return redirect('rbac:department')
        except Exception as error:
            department_data = Department.objects.order_by('id')
            return render(request, self.template_name, {
                "department_data": department_data,
                "view_message": self.view_message,
                "error": error
            })


# 部门列表
class DepartmentListView(View):
    template_name = 'rbac/department.html'
    view_message = "部门列表"

    @method_decorator(login_required)
    def post(self, request):
        department_data = Department.objects.order_by('create_date')
        return render(request, self.template_name, {
            "department_data": department_data,
            "view_message": self.view_message
        })

    @method_decorator(login_required)
    def get(self, request):
        department_data = Department.objects.order_by('create_date')
        return render(request, self.template_name, {
            "department_data": department_data,
            "view_message": self.view_message
        })


# 修改部门信息
class DepartmentEditView(View):
    template_name = 'rbac/department_edit.html'
    view_message = "修改部门信息"

    @method_decorator(login_required)
    def post(self, request, department_id):
        department_data = get_object_or_404(Department, pk=department_id)
        department_register = DepartmentForm(request.POST, instance=department_data)
        if not department_register.is_valid():
            return render(request, self.template_name, {
                "department_register": department_register,
                "view_message": self.view_message
            })
        try:
            department_register.save()
            return redirect('rbac:department')
        except Exception as error:
            return render(request, self.template_name, {
                "department_register": department_register,
                "view_message": self.view_message,
                "error": error
            })

    @method_decorator(login_required)
    def get(self, request, department_id):
        department_data = get_object_or_404(Department, pk=department_id)
        department_register = DepartmentForm(instance=department_data)
        return render(request, self.template_name, {
            "department_register": department_register,
            "view_message": self.view_message
        })
