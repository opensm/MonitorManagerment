from django.conf import settings
from rbac.models import Role


def init_permission(user, request):
    """
    用于做用户登录成功之后，权限信息的初始化。
    :param user: 登录的用户对象
    :param request: 请求相关的对象
    :return:
    """

    """
                [
                    {'permission__title': '用户列表', 'permission__url': '/users/', 'permission__code': 'list', 'permission__group_id': 1}
                    {'permission__title': '添加用户', 'permission__url': '/users/add/', 'permission__code': 'add', 'permission__group_id': 1}
                    {'permission__title': '删除用户', 'permission__url': '/users/del/(\\d+)/', 'permission__code': 'del', 'permission__group_id': 1}
                    {'permission__title': '修改用户', 'permission__url': '/users/edit/(\\d+)/', 'permission__code': 'edit', 'permission__group_id': 1}
                    {'permission__title': '主机列表', 'permission__url': '/hosts/', 'permission__code': 'list', 'permission__group_id': 2}
                    {'permission__title': '添加主机', 'permission__url': '/hosts/add/', 'permission__code': 'add', 'permission__group_id': 2}
                    {'permission__title': '删除主机', 'permission__url': '/hosts/del/(\\d+)/', 'permission__code': 'del', 'permission__group_id': 2}
                    {'permission__title': '修改主机', 'permission__url': '/hosts/edit/(\\d+)/', 'permission__code': 'edit', 'permission__group_id': 2}
                ]

                {
                    1(权限组ID): {
                        urls: [/u sers/,/users/add/ ,/users/del/(\d+)/],
                        codes: [list,add,del]
                    },
                    2: {
                        urls: [/hosts/,/hosts/add/ ,/hosts/del/(\d+)/],
                        codes: [list,add,del]
                    }
                }

                """
    if user.is_superuser:
        permission_list = Role.objects.values(
            'permission__id',  # 权限ID
            'permission__title',  # 权限名称
            'permission__url',  # 权限URL
            'permission__code',  # 权限CODE
            'permission__group_menu_id',  # 组内菜单ID(null表示自己是菜单，1)
            'permission__group_id',  # 权限组ID
            'permission__group__menu__id',  # 一级菜单ID
            'permission__group__menu__name',  # 一级菜单名称
            'permission__group__menu__types',  # 菜单种类
        )
    else:
        permission_list = user.roles.values(
            'permission__id',  # 权限ID
            'permission__title',  # 权限名称
            'permission__url',  # 权限URL
            'permission__code',  # 权限CODE
            'permission__group_menu_id',  # 组内菜单ID(null表示自己是菜单，1)
            'permission__group_id',  # 权限组ID
            'permission__group__menu__id',  # 一级菜单ID
            'permission__group__menu__name',  # 一级菜单名称
            'permission__group__menu__types',  # 菜单种类
        ).distinct()
    # print(permission_list)
    # 获取权限信息+组+菜单，放入session，用于以后在页面上自动生成动态菜单。
    permission_menu_list = []
    for item in permission_list:
        # if item['permission__code'] in ['delete', 'update'] and item['permission__group__menu__types'] != 'current':
        #     continue
        if (item['permission__code'] == "update" and item['permission__group__menu__types'] == 'current') or (
                item['permission__code'] not in ['delete', 'update', 'insert'] and item[
            'permission__group__menu__types'] != 'current'):
            val = {
                'id': item['permission__id'],
                'title': item['permission__title'],
                'url': item['permission__url'],
                'pid': item['permission__group_menu_id'],
                'menu_id': item['permission__group__menu__id'],
                'menu__name': item['permission__group__menu__name'],
                'menu__types': item['permission__group__menu__types'],
            }
            permission_menu_list.append(val)
    request.session[settings.PERMISSION_MENU_SESSION_KEY] = permission_menu_list

    # 获取权限信息，放入session，用于以后在中间件中权限进行匹配

    permission_dict = {}
    for permission in permission_list:
        group_id = permission['permission__group_id']
        url = permission['permission__url']
        code = permission['permission__code']
        if group_id in permission_dict:
            # 头像资源权限
            permission_dict[group_id]['urls'].append("/upload/avatar/%s/.*" % user.id)
            permission_dict[group_id]['urls'].append(url)
            permission_dict[group_id]['codes'].append(code)
        else:
            permission_dict[group_id] = {'urls': [url, ], 'codes': [code, ]}
    print(permission_dict)
    request.session[settings.PERMISSION_DICT_SESSION_KEY] = permission_dict
