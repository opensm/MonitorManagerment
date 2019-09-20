# -*- coding: utf-8 -*-
__author__ = 'YSQ'
from django import forms
from django.forms import Form, ModelForm
from django.forms import fields
from django.forms import widgets
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from .models import *


# 登陆form
class LoginForm(Form):
    username = fields.EmailField(
        label="用户名",
        required=True,
        error_messages={
            'required': '用户名不能为空',
        },
        widget=widgets.TextInput(attrs={'class': 'form-control m-input'})
    )
    password = fields.CharField(
        label='密码',
        required=True,
        error_messages={
            'required': '密码不能为空'
        },
        widget=widgets.PasswordInput(attrs={'class': 'form-control m-input'})
    )


# 修改密码
class PasswordReset(forms.Form):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True, 'class': 'form-control m-input'}),
        required=True,
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autofocus': True, 'class': 'form-control m-input'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        required=True,
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True, 'class': 'form-control m-input'}),
        required=True,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


# 新增用户和修改用户
class UserProfixForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfixForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['username'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['mobile'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['department'].widget.attrs.update({'class': 'form-control m-input'})

    class Meta:
        model = UserInfo
        fields = ['username', 'first_name', 'last_name', 'mobile', 'img', 'department', 'is_active',
                  'is_staff', 'roles']
        widgets = {
            "roles": widgets.CheckboxSelectMultiple(
                attrs={"class": "form-control m-bootstrap-select m_selectpicker"}
            )
        }

    def save(self, commit=True, create=True):
        """
        :param commit:
        :param create:
        :return:
        """
        users = super(UserProfixForm, self).save(commit=True)
        if create:
            users.save()
        elif not create and commit:
            user_profile = UserInfo.objects.get(username=self.cleaned_data['username'])
            user_profile.save()
            user_profile.roles.set("")
            for role in self.cleaned_data['roles']:
                user_profile.roles.add(role)
        else:
            return users
        return users


# 角色修改和添加
class RoleInfoModelForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(RoleInfoModelForm, self).__init__(*args, **kwargs)
    #     self.fields['title'].widget.attrs.update({'class': 'form-control m-input'})
    #     self.fields['permissions'].widget.attrs.update({'class': 'form-control m-input'})

    def save(self, commit=True, create=True):
        """
        :param commit:
        :param create:
        :return:
        """
        role = super(RoleInfoModelForm, self).save(commit=True)
        if create and commit:
            role.save()
        elif not create and commit:
            role_profile = Role.objects.get(title=self.cleaned_data['title'])
            role_profile.save()
            role_profile.permission.set("")
            for permission in self.cleaned_data['permission']:
                role_profile.permission.add(permission.id)
        else:
            return role
        return role

    class Meta:
        model = Role
        fields = ("title", "permission")
        widgets = {
            "title": widgets.TextInput(attrs={"class": "form-control m-input"}),
            "permission": widgets.CheckboxSelectMultiple(
                attrs={"class": "form-control m-input"},
            )
        }

        labels = {
            "title": "角色名称",
            "permission": "权限",
        }


# 菜单修改和添加
class MenuInfoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(MenuInfoForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['types'].widget.attrs.update({'class': 'form-control m-input'})

    class Meta:
        model = Menu
        fields = "__all__"
        exclude = ['create_date']


# 权限组修改和添加
class PermissionGroupForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PermissionGroupForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['menu'].widget.attrs.update({'class': 'form-control m-input'})

    class Meta:
        model = PermissionGroup
        fields = "__all__"
        exclude = ['create_date']


# 权限修改和添加
class PermissionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PermissionForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['url'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['code'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['group'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['group_menu'].widget.attrs.update({'class': 'form-control m-input'})

    def save(self, commit=True):
        permission = super(PermissionForm, self).save(commit=commit)
        permission.url = self.cleaned_data["url"] + ".html"
        if commit:
            permission.save()
        return permission

    class Meta:
        model = Permission
        fields = "__all__"
        exclude = ['create_date']


# 部门修改和添加
class DepartmentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control m-input'})

    class Meta:
        model = Department
        fields = "__all__"
        exclude = ['create_date']
        labels = {
            "title": "部门"
        }
