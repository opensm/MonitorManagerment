from django.urls import path
from rbac import views

app_name = 'rbac'
urlpatterns = [
    # 登陆/登出
    path('login.html', views.UserLoginView.as_view(), name='login'),
    path('logout.html', views.UserLogoutView.as_view(), name='logout'),
    # 用户管理
    path('user/list.html', views.UserListView.as_view(), name='users'),
    path('user/edit/<int:user_id>.html', views.UserEditView.as_view(), name='user_edit'),
    path('user/del/<int:user_id>.html', views.UserDelView.as_view(), name='user_delete'),
    path('user/add.html', views.UserRegisterView.as_view(), name='user_register'),
    path('user/password.html', views.CurrentUserPasswordReset.as_view(), name='password'),
    # 角色管理
    path('role/list.html', views.RoleListView.as_view(), name='roles'),
    path('role/add.html', views.RoleRegisterView.as_view(), name='roles_register'),
    path('role/del/<int:role_id>.html', views.RoleDelView.as_view(), name='roles_delete'),
    path('role/edit/<int:role_id>.html', views.RoleEditView.as_view(), name='roles_edit'),
    # 菜单管理
    path('menu/list.html', views.MenuListView.as_view(), name='menu'),
    path('menu/add.html', views.MenuRegisterView.as_view(), name="menu_register"),
    path('menu/del/<int:menu_id>.html', views.MenuDelView.as_view(), name="menu_delete"),
    path('menu/edit/<int:menu_id>.html', views.MenuEditView.as_view(), name="menu_edit"),
    # 权限管理
    path('permission/list.html', views.PermissionListView.as_view(), name="permission"),
    path('permission/add.html', views.PermissionRegisterView.as_view(), name="permission_register"),
    path('permission/del/<int:permission_id>.html', views.PermissionDelView.as_view(), name="permission_delete"),
    path('permission/edit/<int:permission_id>.html', views.PermissionEditView.as_view(), name="permission_edit"),
    # 权限组管理
    path('permission_group/list.html', views.PermissionGroupListView.as_view(), name='permission_group'),
    path('permission_group/add.html', views.PermissionGroupRegisterView.as_view(), name="permission_group_register"),
    path(
        'permission_group/edit/<int:group_id>.html',
        views.PermissionGroupEditView.as_view(),
        name='permission_group_update'
    ),
    path(
        'permission_group/del/<int:group_id>.html',
        views.PermissionGroupDelView.as_view(),
        name='permission_group_delete'
    ),
    # 部门管理
    path('department/list.html', views.DepartmentListView.as_view(), name='department'),
    path('department/add.html', views.DepartmentRegisterView.as_view(), name="department_register"),
    path('department/del/<int:department_id>.html', views.DepartmentDelView.as_view(), name="department_delete"),
    path('department/edit/<int:department_id>.html', views.DepartmentEditView.as_view(), name="department_edit")
]
